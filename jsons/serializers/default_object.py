from typing import Optional, Callable
from jsons.classes import JsonSerializable
from jsons.serializers.default_dict import default_dict_serializer


def default_object_serializer(
        obj: object,
        key_transformer: Optional[Callable[[str], str]] = None,
        strip_nulls: bool = False,
        strip_privates: bool = False,
        strip_properties: bool = False,
        strip_class_variables: bool = False,
        **kwargs) -> dict:
    """
    Serialize the given ``obj`` to a dict. All values within ``obj`` are also
    serialized. If ``key_transformer`` is given, it will be used to transform
    the casing (e.g. snake_case) to a different format (e.g. camelCase).
    :param obj: the object that is to be serialized.
    :param key_transformer: a function that will be applied to all keys in the
    resulting dict.
    :param strip_nulls: if ``True`` the resulting dict will not contain null
    values.
    :param strip_privates: if ``True`` the resulting dict will not contain
    private attributes (i.e. attributes that start with an underscore).
    :param strip_properties: if ``True`` the resulting dict will not contain
    values from @properties.
    :param strip_class_variables: if ``True`` the resulting dict will not
    contain values from class variables.
    :param kwargs: any keyword arguments that are to be passed to the
    serializer functions.
    :return: a Python dict holding the values of ``obj``.
    """
    obj_dict = _get_dict_from_obj(obj, strip_privates, strip_properties,
                                  strip_class_variables, **kwargs)
    return default_dict_serializer(obj_dict,
                                   key_transformer=key_transformer,
                                   strip_nulls=strip_nulls,
                                   strip_privates=strip_privates,
                                   strip_properties=strip_properties,
                                   strip_class_variables=strip_class_variables,
                                   **kwargs)


def _get_dict_from_obj(obj,
                       strip_privates,
                       strip_properties,
                       strip_class_variables,
                       cls=None, *_, **__):
    excluded_elems = dir(JsonSerializable)
    props, other_cls_vars = _get_class_props(obj.__class__)
    return {attr: obj.__getattribute__(attr) for attr in dir(obj)
            if not attr.startswith('__')
            and not (strip_privates and attr.startswith('_'))
            and not (strip_properties and attr in props)
            and not (strip_class_variables and attr in other_cls_vars)
            and attr != 'json'
            and not isinstance(obj.__getattribute__(attr), Callable)
            and (not cls or attr in cls.__slots__)
            and attr not in excluded_elems}


def _get_class_props(cls):
    props = []
    other_cls_vars = []
    for n, v in _get_complete_class_dict(cls).items():
        props.append(n) if type(v) is property else other_cls_vars.append(n)
    return props, other_cls_vars


def _get_complete_class_dict(cls):
    cls_dict = {}
    # Loop reversed so values of sub-classes override those of super-classes.
    for cls_or_elder in reversed(cls.mro()):
        cls_dict.update(cls_or_elder.__dict__)
    return cls_dict
