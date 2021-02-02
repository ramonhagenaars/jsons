from datetime import date

from jsons._datetime_impl import to_str, RFC3339_TIME_PATTERN


def default_time_serializer(obj: date, **kwargs) -> str:
    """
    Serialize the given time instance to a string. It uses the RFC3339
    pattern.
    :param obj: the time instance that is to be serialized.
    :param kwargs: not used.
    :return: ``time`` as an RFC3339 string.
    """
    return to_str(obj, False, kwargs['fork_inst'],
                  RFC3339_TIME_PATTERN)
