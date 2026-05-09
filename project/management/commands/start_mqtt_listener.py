"""
Django management command: run the MQTT subscriber and persist panel power (KW) to DB.
Runs until process is killed. Use with systemd for always-on deployment.
"""

import logging
import sys

from django.core.management.base import BaseCommand

from project.mqtt.client import build_client

logger = logging.getLogger(__name__)


def configure_logging(verbosity: int) -> None:
    """Configure root and project loggers; output to stderr."""
    level = logging.DEBUG if verbosity > 1 else (logging.INFO if verbosity else logging.WARNING)
    fmt = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(logging.Formatter(fmt))
    root = logging.getLogger()
    root.setLevel(level)
    if not root.handlers:
        root.addHandler(handler)
    for name in ("project.mqtt", "project.services.power_service"):
        logging.getLogger(name).setLevel(level)


class Command(BaseCommand):
    help = "Start MQTT listener: subscribe to panels/voltage, store KW to Panel and PanelPowerReading."

    def add_arguments(self, parser):
        parser.add_argument(
            "--no-loop",
            action="store_true",
            help="Connect and subscribe then exit (for testing).",
        )

    def handle(self, *args, **options):
        configure_logging(options["verbosity"])
        try:
            client = build_client()
            if options.get("no_loop"):
                import time
                client.loop_start()
                time.sleep(2)
                client.loop_stop()
                client.disconnect()
                return
            client.loop_forever()
        except KeyboardInterrupt:
            logger.info("MQTT listener stopped by user")
        except Exception as e:
            logger.exception("MQTT listener failed: %s", e)
            raise
