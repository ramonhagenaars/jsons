from jsons.exceptions import UnfulfilledArgumentError
from jsons._main_impl import load


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
    tuple_types = getattr(cls, '__tuple_params__', cls.__args__)
    if len(tuple_types) > 1 and tuple_types[1] is ...:
        tuple_types = [tuple_types[0]] * len(obj)
    list_ = [load(value, tuple_types[i], **kwargs)
             for i, value in enumerate(obj)]
    return tuple(list_)


def default_namedtuple_deserializer(obj: list, cls: type, **kwargs) -> object:
    """
    Deserialize a (JSON) list into a named tuple by deserializing all items of
    that list.
    :param obj: the tuple that needs deserializing.
    :param cls: the NamedTuple.
    :param kwargs: any keyword arguments.
    :return: a deserialized named tuple (i.e. an instance of a class).
    """
    args = []
    for index, field_name in enumerate(cls._fields):
        if index < len(obj):
            field = obj[index]
        else:
            field = cls._field_defaults.get(field_name, None)
        if not field:
            msg = ('No value present in {} for argument "{}"'
                   .format(obj, field_name))
            raise UnfulfilledArgumentError(msg, field_name, obj, cls)
        cls_ = cls._field_types.get(field_name, None)
        loaded_field = load(field, cls_, **kwargs)
        args.append(loaded_field)
    inst = cls(*args)
    return inst
