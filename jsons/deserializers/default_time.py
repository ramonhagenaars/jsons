from datetime import time

from jsons._datetime_impl import get_datetime_inst, RFC3339_TIME_PATTERN


def default_time_deserializer(obj: str,
                              cls: type = time,
                              **kwargs) -> time:
    """
    Deserialize a string with an RFC3339 pattern to a time instance.
    :param obj: the string that is to be deserialized.
    :param cls: not used.
    :param kwargs: not used.
    :return: a ``datetime.time`` instance.
    """
    return get_datetime_inst(obj, RFC3339_TIME_PATTERN).time()
