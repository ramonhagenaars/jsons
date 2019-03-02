from datetime import datetime
from typing import Optional
from jsons._datetime_impl import get_offset_str
from jsons._main_impl import RFC3339_DATETIME_PATTERN


def default_datetime_serializer(obj: datetime,
                                strip_microseconds: Optional[bool] = True,
                                **kwargs) -> str:
    """
    Serialize the given datetime instance to a string. It uses the RFC3339
    pattern. If datetime is a localtime, an offset is provided. If datetime is
    in UTC, the result is suffixed with a 'Z'.
    :param obj: the datetime instance that is to be serialized.
    :param strip_microseconds: determines whether microseconds should be
    omitted.
    :param kwargs: not used.
    :return: ``datetime`` as an RFC3339 string.
    """
    pattern = RFC3339_DATETIME_PATTERN
    offset = get_offset_str(obj)
    if not strip_microseconds and obj.microsecond:
        pattern += '.%f'
    return obj.strftime("{}{}".format(pattern, offset))
