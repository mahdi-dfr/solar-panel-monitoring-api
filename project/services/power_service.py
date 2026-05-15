"""
Service layer for storing panel power data from MQTT.
Decouples MQTT handling from Django ORM.
"""

import logging
from decimal import Decimal, InvalidOperation
from django.db import transaction
from django.utils import timezone

from project.models import Panel

logger = logging.getLogger(__name__)


def parse_kw_value(raw: str):
    """
    Convert KW string from payload to numeric value.
    Returns (int_value for Panel.kw, decimal_value for PanelPowerReading) or (None, None) on error.
    """
    if raw is None or (isinstance(raw, str) and not raw.strip()):
        return None, None
    try:
        if isinstance(raw, (int, float)):
            d = Decimal(str(raw))
        else:
            d = Decimal(str(raw).strip())
        int_val = int(d) if d == d.to_integral_value() else int(round(d))
        return int_val, d
    except (InvalidOperation, ValueError, TypeError) as e:
        logger.warning("Invalid KW value: %r, error: %s", raw, e)
        return None, None


# def store_power_for_board(board_id: int, kw_raw) -> bool:
#     """
#     Idempotent store of power for a board: update Panel.kw and append PanelPowerReading.
#     Uses second-resolution recorded_at for idempotency (same second overwrites).
#     Returns True if stored, False if panel not found or invalid kw.
#     """
#     int_kw, decimal_kw = parse_kw_value(kw_raw)
#     if decimal_kw is None:
#         return False

#     try:
#         panel = Panel.objects.get(board_id=board_id)
#     except Panel.DoesNotExist:
#         logger.warning("Panel with board_id=%s not found, skipping power store", board_id)
#         return False
#     except Panel.MultipleObjectsReturned:
#         panel = Panel.objects.filter(board_id=board_id).first()
#         logger.warning("Multiple panels with board_id=%s, using panel pk=%s", board_id, panel.pk)

#     recorded_at = timezone.now().replace(microsecond=0)

#     try:
#         with transaction.atomic():
#             Panel.objects.filter(pk=panel.pk).update(kw=int_kw, update_at=recorded_at)
#             PanelPowerReading.objects.update_or_create(
#                 panel=panel,
#                 recorded_at=recorded_at,
#                 defaults={"kw": decimal_kw},
#             )
#         logger.debug("Stored power board_id=%s kw=%s at %s", board_id, decimal_kw, recorded_at)
#         return True
#     except Exception as e:
#         logger.exception("Failed to store power for board_id=%s: %s", board_id, e)
#         return False
