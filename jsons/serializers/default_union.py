from typing import Union
from jsons._common_impl import get_class_name
from jsons._compatibility_impl import get_union_params
from jsons._dump_impl import dump
from jsons.exceptions import JsonsError, SerializationError


def default_union_serializer(obj: object, cls: Union, **kwargs) -> object:
    """
    Serialize an object to any matching type of the given union. The first
    successful serialization is returned.
    :param obj: The object that is to be serialized.
    :param cls: The Union type with a generic (e.g. Union[str, int]).
    :param kwargs: Any keyword arguments that are passed through the
    serialization process.
    :return: An object of the first type of the Union that could be
    serialized successfully.
    """
    for sub_type in get_union_params(cls):
        try:
            return dump(obj, sub_type, **kwargs)
        except JsonsError:
            pass  # Try the next one.
    else:
        args_msg = ', '.join([get_class_name(cls_)
                              for cls_ in get_union_params(cls)])
        err_msg = ('Could not match the object of type "{}" to any type of '
                   'the Union: {}'.format(str(cls), args_msg))
        raise SerializationError(err_msg)
