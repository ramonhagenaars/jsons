"""
PRIVATE MODULE: do not import (from) it directly.

This module contains functionality for ``date`` related stuff.
"""
from datetime import date, datetime


RFC3339_DATETIME_PATTERN = '{}-{:02d}-{:02d}T00:00:00'
DATE_PARSE_PATTERN = '%Y-%m-%d'


def to_str(
        dt: date,
        pattern: str = RFC3339_DATETIME_PATTERN) -> str:

    return pattern.format(dt.year, dt.month, dt.day)


def get_date_inst(obj: str, pattern: str) -> datetime:
    """
    Return a date instance with timezone info from the given ``obj``.
    :param obj: the ``obj`` in RFC3339 format.
    :param pattern: the date pattern.
    :return: a date instance.
    """
    return datetime.strptime(obj, pattern).date()

