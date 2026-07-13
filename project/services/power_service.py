import logging

from django.db import transaction

from project.models import (
    Board,
    String,
    BoardReading,
    StringReading,
)

logger = logging.getLogger(__name__)


def store_mqtt_payload(data: dict):
    print('12121212')
    print(data)

    board_id = data.get("Voltage_board_id")

    if board_id is None:
        logger.warning("Missing Voltage_board_id")
        return False

    try:
        board = Board.objects.get(board_id=board_id)
    except Board.DoesNotExist:
        logger.warning("Board not found: %s", board_id)
        return False

    temperature = data.get("Temp")
    humidity = data.get("Hum")

    strings_data = data.get("Strings", [])

    try:
        with transaction.atomic():

            board_reading = BoardReading.objects.create(
                board=board,
                temperature=temperature or 0,
                humidity=humidity or 0,
            )

            for item in strings_data:

                string_id = item.get("String_id")

                if string_id is None:
                    logger.warning("Missing String_id in item: %r", item)
                    continue

                try:
                    string = String.objects.get(
                        board=board,
                        string_id=string_id
                    )
                except String.DoesNotExist:
                    logger.warning(
                        "String not found board=%s string=%s",
                        board_id,
                        string_id
                    )
                    continue

                # پشتیبانی از هر دو حالت "Current" و "current" چون در نسخه‌ی
                # قبلی کد فقط "current" (حرف کوچک) خونده می‌شد و اگر دستگاه
                # واقعی "Current" (حرف بزرگ، هماهنگ با بقیه‌ی فیلدها) بفرسته،
                # مقدار همیشه 0 ذخیره می‌شد بدون هیچ خطایی.
                current_value = item.get("Current", item.get("current", 0))

                StringReading.objects.create(
                    board_reading=board_reading,
                    string=string,
                    voltage=item.get("Voltage", 0),
                    current=current_value,
                    power=item.get("Power", 0),
                    energy=item.get("Energy", 0),
                )

        logger.info("Stored MQTT data for board=%s", board_id)
        return True

    except Exception as e:
        logger.exception("Failed storing MQTT payload: %s", e)
        return False