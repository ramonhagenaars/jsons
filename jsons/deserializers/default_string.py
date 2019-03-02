from datetime import datetime
from typing import Optional
from jsons.exceptions import DeserializationError
from jsons._main_impl import load


def default_string_deserializer(obj: str,
                                cls: Optional[type] = None,
                                **kwargs) -> object:
    """
    Deserialize a string. If the given ``obj`` can be parsed to a date, a
    ``datetime`` instance is returned.
    :param obj: the string that is to be deserialized.
    :param cls: not used.
    :param kwargs: any keyword arguments.
    :return: the deserialized obj.
    """
    try:
        result = load(obj, datetime, **kwargs)
    except DeserializationError:
        result = obj
    return result
