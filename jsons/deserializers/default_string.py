from datetime import datetime
from typing import Optional

from jsons._load_impl import load
from jsons.deserializers.default_primitive import default_primitive_deserializer
from jsons.exceptions import DeserializationError


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
    target_is_str = cls is str and not kwargs.get('_inferred_cls')
    if target_is_str:
        return str(obj)
    try:
        result = load(obj, datetime, **kwargs)
    except DeserializationError:
        result = default_primitive_deserializer(obj, str)
    return result
