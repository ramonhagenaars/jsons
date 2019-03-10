from typing import Optional, Callable
from jsons._common_impl import get_class_name, META_ATTR
from jsons.classes import JsonSerializable
from jsons.serializers.default_dict import default_dict_serializer


def default_object_serializer(
        obj: object,
        key_transformer: Optional[Callable[[str], str]] = None,
        strip_nulls: bool = False,
        strip_privates: bool = False,
        strip_properties: bool = False,
        strip_class_variables: bool = False,
        verbose: bool = False,
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
    :param verbose: if ``True`` the resulting dict will contain meta
    information (e.g. on how to deserialize).
    :param kwargs: any keyword arguments that are to be passed to the
    serializer functions.
    :return: a Python dict holding the values of ``obj``.
    """
    cls = kwargs['cls'] or obj.__class__
    obj_dict = _get_dict_from_obj(obj, strip_privates, strip_properties,
                                  strip_class_variables, **kwargs)
    kwargs_ = {**kwargs}
    if verbose:
        kwargs_['store_cls'] = True
    result = default_dict_serializer(
        obj_dict,
        key_transformer=key_transformer,
        strip_nulls=strip_nulls,
        strip_privates=strip_privates,
        strip_properties=strip_properties,
        strip_class_variables=strip_class_variables,
        **kwargs_)
    cls_name = get_class_name(cls, fully_qualified=True,
                              fork_inst=kwargs['fork_inst'])
    if kwargs.get('store_cls'):
        result['-cls'] = cls_name
    elif verbose:
        result = _get_dict_with_meta(result, cls_name)
    return result


def _get_dict_from_obj(obj,
                       strip_privates,
                       strip_properties,
                       strip_class_variables,
                       cls=None, *_, **__) -> dict:
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


def _get_dict_with_meta(obj: dict, cls_name: str) -> dict:
    # This function will add a -meta section to the given obj (provided that
    # the given obj has -cls attributes for all children).
    def _fill_collection_of_types(obj_: dict,
                                  cls_name_: Optional[str],
                                  prefix: str,
                                  collection_of_types_: dict) -> str:
        # This function loops through obj to fill collection_of_types_ with the
        # class names.
        cls_name_ = cls_name_ or obj_.pop('-cls')
        for attr in obj_:
            if isinstance(obj_[attr], dict):
                attr_class = _fill_collection_of_types(obj_[attr],
                                                       None,
                                                       prefix + attr + '/',
                                                       collection_of_types_)
                collection_of_types_[prefix + attr] = attr_class
        return cls_name_

    collection_of_types = {}
    _fill_collection_of_types(obj, cls_name, '/', collection_of_types)
    collection_of_types['/'] = cls_name
    obj[META_ATTR] = {
        'classes': collection_of_types
    }
    return obj
