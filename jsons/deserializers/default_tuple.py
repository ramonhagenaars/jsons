from typing import Union
from typish import get_args
from jsons._common_impl import NoneType
from jsons._compatibility_impl import tuple_with_ellipsis, get_union_params
from jsons._load_impl import load
from jsons.exceptions import UnfulfilledArgumentError


def default_tuple_deserializer(obj: list,
                               cls: type = None,
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
        return default_namedtuple_deserializer(obj, cls, **kwargs)
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
    args = []
    for index, field_name in enumerate(cls._fields):
        if index < len(obj):
            key = field_name if is_dict else index
            field = obj[key]
        else:
            field = cls._field_defaults.get(field_name, None)

        if field is None:
            hint = getattr(cls, '_field_types', {}).get(field_name)
            if NoneType not in (get_union_params(hint) or []):
                # The value 'None' is not permitted here.
                msg = ('No value present in {} for argument "{}"'
                       .format(obj, field_name))
                raise UnfulfilledArgumentError(msg, field_name, obj, cls)
        field_types = getattr(cls, '_field_types', None)
        cls_ = field_types.get(field_name) if field_types else None
        loaded_field = load(field, cls_, **kwargs)
        args.append(loaded_field)
    inst = cls(*args)
    return inst
