from typing import Union

from jsons._common_impl import get_class_name
from jsons._compatibility_impl import get_union_params
from jsons._load_impl import load
from jsons.exceptions import JsonsError, DeserializationError


def default_union_deserializer(obj: object, cls: Union, **kwargs) -> object:
    """
    Deserialize an object to any matching type of the given union. The first
    successful deserialization is returned.
    :param obj: The object that needs deserializing.
    :param cls: The Union type with a generic (e.g. Union[str, int]).
    :param kwargs: Any keyword arguments that are passed through the
    deserialization process.
    :return: An object of the first type of the Union that could be
    deserialized successfully.
    """
    for sub_type in get_union_params(cls):
        try:
            return load(obj, sub_type, **kwargs)
        except JsonsError:
            pass  # Try the next one.
    else:
        args_msg = ', '.join([get_class_name(cls_)
                              for cls_ in get_union_params(cls)])
        err_msg = ('Could not match the object of type "{}" to any type of '
                   'the Union: {}'.format(type(obj).__name__, args_msg))
        raise DeserializationError(err_msg, obj, cls)
