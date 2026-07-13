"""
Production MQTT subscriber for solar panel voltage/power messages.
Uses paho-mqtt with persistent session, QoS 1, auto-reconnect.
Credentials and TLS from environment; no hardcoded secrets.
"""

import json
import logging
import os
import ssl

import paho.mqtt.client as mqtt

from project.services.power_service import store_mqtt_payload

logger = logging.getLogger(__name__)

MQTT_TOPIC = os.getenv("MQTT_TOPIC", "panels/voltage")
MQTT_QOS = 1


def _parse_payload(payload: bytes) -> dict | None:
    """Parse JSON payload; return None on failure."""
    if not payload:
        return None
    try:
        return json.loads(payload.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        logger.warning("Invalid JSON in MQTT message: %s", e)
        return None


def _on_connect(client, userdata, flags, rc):
    """Callback when broker connects (CallbackAPIVersion.VERSION1: rc int)."""
    if rc == 0:
        logger.info("MQTT connected to broker")
        # subscribe دوباره اینجا هم انجام می‌شه (idempotent است) تا اگر
        # session روی بروکر expire/reset بشه، دریافت پیام قطع نشه.
        client.subscribe(MQTT_TOPIC, qos=MQTT_QOS)
        logger.info("Subscribed to topic: %s (qos=%s)", MQTT_TOPIC, MQTT_QOS)
    else:
        logger.warning("MQTT connect failed, rc=%s", rc)


def _on_disconnect(client, userdata, rc):
    """Callback when broker disconnects."""
    logger.warning("MQTT disconnected, rc=%s", rc)


def on_message(client, userdata, msg):
    data = _parse_payload(msg.payload)
    if data is None:
        return
    try:
        store_mqtt_payload(data)
    except Exception as e:
        logger.exception("Failed to process MQTT message: %s", e)


def build_client() -> mqtt.Client:
    """Build and configure MQTT client from environment. Supports MQTT v5 and v3."""
    use_v5 = os.getenv("MQTT_USE_V5", "0").strip().lower() in ("1", "true", "yes")
    client = mqtt.Client(
        mqtt.CallbackAPIVersion.VERSION1,
        client_id=os.getenv("MQTT_CLIENT_ID", "solar-monitoring-api"),
        clean_session=False,
        protocol=mqtt.MQTTv5 if use_v5 else mqtt.MQTTv311,
    )
    client.on_connect = _on_connect
    client.on_disconnect = _on_disconnect
    client.on_message = on_message

    # =====================================================================
    # اطلاعات سرور MQTT از اینجا (Environment Variables) خونده می‌شه.
    # این‌ها رو کد وارد نکن! توی فایل .env پروژه (کنار manage.py) ست کن:
    #
    #   MQTT_HOST=آدرس یا IP بروکر شما
    #   MQTT_PORT=1883        (یا 8883 اگر TLS فعاله)
    #   MQTT_USERNAME=یوزرنیم بروکر (در صورت نیاز)
    #   MQTT_PASSWORD=پسورد بروکر (در صورت نیاز)
    #   MQTT_USE_TLS=0
    #   MQTT_TOPIC=panels/voltage
    #   MQTT_CLIENT_ID=solar-monitoring-api
    # =====================================================================
    host = os.getenv("MQTT_HOST", "localhost")
    port = int(os.getenv("MQTT_PORT", "1883"))
    username = os.getenv("MQTT_USERNAME")
    password = os.getenv("MQTT_PASSWORD")
    use_tls = os.getenv("MQTT_USE_TLS", "0").strip().lower() in ("1", "true", "yes")

    if username:
        client.username_pw_set(username, password or None)
    if use_tls:
        tls = ssl.create_default_context()
        tls_insecure = os.getenv("MQTT_TLS_INSECURE", "0").strip().lower() in ("1", "true", "yes")
        client.tls_set_context(tls)
        if tls_insecure:
            client.tls_insecure_set(True)
        if port == 1883:
            port = 8883

    client.connect(host, port, keepalive=60)
    client.reconnect_delay_set(min_delay=1, max_delay=120)
    client.subscribe(MQTT_TOPIC, qos=MQTT_QOS)
    return client