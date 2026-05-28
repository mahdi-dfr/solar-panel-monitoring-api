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

    board_id = data.get("Voltage_board_id")

    if not board_id:
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

            # ساخت BoardReading
            board_reading = BoardReading.objects.create(
                board=board,
                temperature=temperature or 0,
                humidity=humidity or 0,
            )

            # ساخت StringReading ها
            for item in strings_data:

                string_id = item.get("String_id")

                if not string_id:
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

                StringReading.objects.create(
                    board_reading=board_reading,
                    string=string,

                    voltage=item.get("Voltage", 0),
                    current=item.get("current", 0),

                    power=item.get("Power", 0),
                    energy=item.get("Energy", 0),
                )

        logger.info(
            "Stored MQTT data for board=%s",
            board_id
        )

        return True

    except Exception as e:

        logger.exception(
            "Failed storing MQTT payload: %s",
            e
        )

        return False