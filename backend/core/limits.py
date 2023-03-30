"""Служебные константы"""

from enum import Enum, IntEnum


class Limits(IntEnum):
    """Лимиты ограничений полей"""
    LEN_NAME_LIMIT = 200
    LEN_USERS_NAME_LIMIT = 150
    LEN_USERS_PASSWORD_LIMIT = 150
    LEN_EMAIL_LIMIT = 254
    LEN_HEX_CODE_LIMIT = 7
    LEN_TEXT_LIMIT = 5000
    MIN_COOKING_TIME = 1
    MAX_COOKING_TIME = 500
    MIN_AMOUNT_INGREDIENTS = 1