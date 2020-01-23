from typing import Union, Optional, Tuple

from typish import get_args

from jsons._compatibility_impl import tuple_with_ellipsis
from jsons._dump_impl import dump
from jsons.serializers.default_iterable import default_iterable_serializer


def default_tuple_serializer(obj: tuple,
                             cls: Optional[type] = None,
                             **kwargs) -> Union[list, dict]:
    """
    Serialize the given ``obj`` to a list of serialized objects.
    :param obj: the tuple that is to be serialized.
    :param cls: the type of the ``obj``.
    :param kwargs: any keyword arguments that may be given to the serialization
    process.
    :return: a list of which all elements are serialized.
    """
    if hasattr(obj, '_fields'):
        return default_namedtuple_serializer(obj, **kwargs)

    cls_ = cls
    if cls and tuple_with_ellipsis(cls):
        cls_ = Tuple[(get_args(cls)[0],) * len(obj)]

    return default_iterable_serializer(obj, cls_, **kwargs)


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
