from datetime import datetime
from typing import Optional

from jsons._datetime_impl import to_str, RFC3339_DATETIME_PATTERN


def default_datetime_serializer(obj: datetime,
                                *,
                                strip_microseconds: Optional[bool] = False,
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
    return to_str(obj, strip_microseconds, kwargs['fork_inst'],
                  RFC3339_DATETIME_PATTERN)
