"""
PRIVATE MODULE: do not import (from) it directly.

This module contains functionality for ``datetime`` related stuff.
"""
from datetime import datetime, timezone, timedelta, time, date
from typing import Union


def get_offset_str(obj: Union[datetime, timedelta]) -> str:
    """
    Return the textual offset of the given ``obj``.
    :param obj: a datetime or timedelta instance.
    :return: the offset following RFC3339.
    """
    func = (_datetime_offset_str if isinstance(obj, datetime)
            else _timedelta_offset_str)
    return func(obj)


def get_datetime_inst(obj: str, pattern: str) -> datetime:
    """
    Return a datetime instance with timezone info from the given ``obj``.
    :param obj: the ``obj`` in RFC3339 format.
    :param pattern: the datetime pattern.
    :return: a datetime instance with timezone info.
    """
    func = _datetime_utc_inst if obj[-1] == 'Z' else _datetime_offset_inst
    return func(obj, pattern)


def _datetime_offset_str(obj: datetime) -> str:
    """
    Return a textual offset (e.g. +01:00 or Z) for the given datetime.
    :param obj: the datetime instance.
    :return: the offset for ``obj``.
    """
    tzone = obj.tzinfo
    if not tzone:
        # datetimes without tzinfo are treated as local times.
        tzone = datetime.now(timezone.utc).astimezone().tzinfo
        if tzone is timezone.utc or tzone.utc is timezone.utc:
            return '+00:00'
    offset = 'Z'
    if tzone.tzname(None) not in ('UTC', 'UTC+00:00'):
        tdelta = tzone.utcoffset(None) or tzone.adjusted_offset
        offset = _timedelta_offset_str(tdelta)
    return offset


def _timedelta_offset_str(tdelta: timedelta) -> str:
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


def _datetime_utc_inst(obj: str, pattern: str) -> datetime:
    """
    Return a datetime instance with UTC timezone info.
    :param obj: a datetime in RFC3339 format.
    :param pattern: the datetime pattern that is used.
    :return: a datetime instance with timezone info.
    """
    dattim_str = obj[0:-1]
    dattim_obj = datetime.strptime(dattim_str, pattern)
    return _new_datetime(dattim_obj.date(), dattim_obj.time(), timezone.utc)


def _datetime_offset_inst(obj: str, pattern: str) -> datetime:
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
    return _new_datetime(dattim_obj.date(), dattim_obj.time(), tz)


def _new_datetime(date_inst: date, time_inst: time, tzinfo: timezone):
    """
    Return a datetime instance from a date, time and timezone.

    This function was required due to the missing argument for tzinfo under the
    Linux Python distribution.
    :param date_inst: the date.
    :param time_inst: the time.
    :param tzinfo: the Timezone.
    :return: a combined datetime instance.
    """
    return datetime.combine(date_inst, time_inst).replace(tzinfo=tzinfo)
