"""
PRIVATE MODULE: do not import (from) it directly.

This module contains functionality for ``datetime`` related stuff.
"""
from datetime import datetime, timezone, timedelta, time


def datetime_offset(obj: datetime) -> str:
    """
    Return a textual offset (e.g. +01:00 or Z) for the given datetime.
    :param obj: the datetime instance.
    :return: the offset for ``obj``.
    """
    tzone = obj.tzinfo
    if not tzone:
        # datetimes without tzinfo are treated as local times.
        tzone = obj.astimezone().tzinfo
        if tzone is timezone.utc:
            return '+00:00'
    offset = 'Z'
    if tzone.tzname(None) not in ('UTC', 'UTC+00:00'):
        tdelta = tzone.utcoffset(None) or tzone.adjusted_offset
        offset = timedelta_offset(tdelta)
    return offset


def timedelta_offset(tdelta: timedelta) -> str:
    """
    Return a textual offset (e.g. +01:00 or Z) for the given timedelta.
    :param tdelta: the timedelta instance.
    :return: the offset for ``tdelta``.
    """
    offset_s = tdelta.total_seconds()
    offset_h = int(offset_s / 3600)
    offset_m = int((offset_s / 60) % 60)
    offset_t = time(abs(offset_h), abs(offset_m))
    operator = '+' if offset_s > 0 else '-'
    offset = offset_t.strftime('{}%H:%M'.format(operator))
    return offset


def datetime_utc(obj: str, pattern: str) -> datetime:
    """
    Return a datetime instance with UTC timezone info.
    :param obj: a datetime in RFC3339 format.
    :param pattern: the datetime pattern that is used.
    :return: a datetime instance with timezone info.
    """
    dattim_str = obj[0:-1]
    dattim_obj = datetime.strptime(dattim_str, pattern)
    return datetime.combine(dattim_obj.date(), dattim_obj.time(), timezone.utc)


def datetime_with_tz(obj: str, pattern: str) -> datetime:
    """
    Return a datetime instance with timezone info.
    :param obj: a datetime in RFC3339 format.
    :param pattern: the datetime pattern that is used.
    :return: a datetime instance with timezone info.
    """
    dat_str, tim_str = obj.split('T')
    splitter, factor = ('+', 1) if '+' in tim_str else ('-', -1)
    naive_tim_str, offset = tim_str.split(splitter)
    naive_dattim_str = '{}T{}'.format(dat_str, naive_tim_str)
    dattim_obj = datetime.strptime(naive_dattim_str, pattern)
    hrs_str, mins_str = offset.split(':')
    hrs = int(hrs_str) * factor
    mins = int(mins_str) * factor
    tz = timezone(offset=timedelta(hours=hrs, minutes=mins))
    return datetime.combine(dattim_obj.date(), dattim_obj.time(), tz)
