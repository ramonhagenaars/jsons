from typing import Callable, Optional, Union

from typish import get_args

from jsons._common_impl import NoneType
from jsons._compatibility_impl import (get_type_hints, get_union_params,
                                       tuple_with_ellipsis)
from jsons._load_impl import load
from jsons.exceptions import UnfulfilledArgumentError


def default_tuple_deserializer(obj: list,
                               cls: type = None,
                               *,
                               key_transformer: Optional[Callable[[str], str]] = None,
                               **kwargs) -> object:
    """
    Deserialize a (JSON) list into a tuple by deserializing all items of that
    list.
    :param obj: the tuple that needs deserializing.
    :param cls: the type optionally with a generic (e.g. Tuple[str, int]).
    :param kwargs: any keyword arguments.
    :return: a deserialized tuple instance.
    """
    if hasattr(cls, '_fields'):
        return default_namedtuple_deserializer(obj, cls, key_transformer=key_transformer, **kwargs)
    cls_args = get_args(cls)
    if cls_args:
        tuple_types = getattr(cls, '__tuple_params__', cls_args)
        if tuple_with_ellipsis(cls):
            tuple_types = [tuple_types[0]] * len(obj)
        list_ = [load(value, tuple_types[i], **kwargs)
                 for i, value in enumerate(obj)]
    else:
        list_ = [load(value, **kwargs) for i, value in enumerate(obj)]
    return tuple(list_)


def default_namedtuple_deserializer(
        obj: Union[list, dict],
        cls: type,
        *,
        key_transformer: Optional[Callable[[str], str]] = None,
        **kwargs) -> object:
    """
    Deserialize a (JSON) list or dict into a named tuple by deserializing all
    items of that list/dict.
    :param obj: the tuple that needs deserializing.
    :param cls: the NamedTuple.
    :param kwargs: any keyword arguments.
    :return: a deserialized named tuple (i.e. an instance of a class).
    """
    is_dict = isinstance(obj, dict)
    key_tfr = key_transformer or (lambda key: key)

    if is_dict:
        tfm_obj = {key_tfr(k): v for k, v in obj.items()}

    args = []
    for index, field_name in enumerate(cls._fields):
        if index < len(obj):
            if is_dict:
                field = tfm_obj[field_name]
            else:
                field = obj[index]
        else:
            field = cls._field_defaults.get(field_name, None)

        # _field_types has been deprecated in favor of __annotations__ in Python 3.8
        if hasattr(cls, '__annotations__'):
            # It is important to use get_type_hints so that forward references get resolved,
            # rather than access __annotations__ directly
            field_types = get_type_hints(cls)
        else:
            field_types = getattr(cls, '_field_types', {})

        if field is None:
            hint = field_types.get(field_name)
            if NoneType not in (get_union_params(hint) or []):
                # The value 'None' is not permitted here.
                msg = ('No value present in {} for argument "{}"'
                       .format(obj, field_name))
                raise UnfulfilledArgumentError(msg, field_name, obj, cls)
        cls_ = field_types.get(field_name) if field_types else None
        loaded_field = load(field, cls_, key_transformer=key_transformer, **kwargs)
        args.append(loaded_field)
    inst = cls(*args)
    return inst
