from typing import Union
from jsons._dump_impl import dump
from jsons.serializers.default_iterable import default_iterable_serializer


def default_tuple_serializer(obj: tuple, **kwargs) -> Union[list, dict]:
    """
    Serialize the given ``obj`` to a list of serialized objects.
    :param obj: the tuple that is to be serialized.
    :param kwargs: any keyword arguments that may be given to the serialization
    process.
    :return: a list of which all elements are serialized.
    """
    if hasattr(obj, '_fields'):
        return default_namedtuple_serializer(obj, **kwargs)
    return default_iterable_serializer(obj, **kwargs)


def default_namedtuple_serializer(obj: tuple, **kwargs) -> dict:
    """
    Serialize the given ``obj`` to a dict of serialized objects.
    :param obj: the named tuple that is to be serialized.
    :param kwargs: any keyword arguments that may be given to the serialization
    process.
    :return: a dict of which all elements are serialized.
    """
    result = {field_name: dump(getattr(obj, field_name), **kwargs)
              for field_name in obj._fields}
    return result
