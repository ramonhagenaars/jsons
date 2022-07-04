from typing import Literal, Any

from jsons._dump_impl import dump

def default_literal_serializer(obj: Any, cls: Literal, **kwargs):
    """
    Serialize an object to its value.
    :param obj: The object that is to be serialized.
    :param cls: The Literal type with values (e.g. Union[1, 2]). Not used.
    :param kwargs: Any keyword arguments that are passed through the
    serialization process.
    :return: The serialized object.
    """
    return dump(obj, type(obj), **kwargs)
