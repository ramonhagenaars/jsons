from datetime import datetime, timezone
from typing import Optional, Callable, Union, MutableSequence, Tuple
from jsons._common_impl import get_class_name, META_ATTR
from jsons._datetime_impl import to_str
from jsons.classes import JsonSerializable
from jsons.classes.verbosity import Verbosity
from jsons.serializers.default_dict import default_dict_serializer


def default_object_serializer(
        obj: object,
        cls: Optional[type] = None,
        *,
        key_transformer: Optional[Callable[[str], str]] = None,
        strip_nulls: bool = False,
        strip_privates: bool = False,
        strip_properties: bool = False,
        strip_class_variables: bool = False,
        strip_attr: Union[str, MutableSequence[str], Tuple[str]] = None,
        verbose: Union[Verbosity, bool] = False,
        **kwargs) -> dict:
    """
    Serialize the given ``obj`` to a dict. All values within ``obj`` are also
    serialized. If ``key_transformer`` is given, it will be used to transform
    the casing (e.g. snake_case) to a different format (e.g. camelCase).
    :param obj: the object that is to be serialized.
    :param cls: the type of the object that is to be dumped.
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
    :param strip_attr: can be a name or a collection of names of attributes
    that are not to be included in the dump.
    dict will not contain attributes with
    :param verbose: if ``True`` the resulting dict will contain meta
    information (e.g. on how to deserialize).
    :param kwargs: any keyword arguments that are to be passed to the
    serializer functions.
    :return: a Python dict holding the values of ``obj``.
    """
    if obj is None:
        return obj
    strip_attr = strip_attr or []
    if (not isinstance(strip_attr, MutableSequence)
            and not isinstance(strip_attr, tuple)):
        strip_attr = (strip_attr,)
    cls = cls or obj.__class__
    obj_dict = _get_dict_from_obj(obj, cls, strip_privates, strip_properties,
                                  strip_class_variables, strip_attr, **kwargs)
    kwargs_ = {**kwargs, 'verbose': verbose}
    verbose = Verbosity.from_value(verbose)
    if Verbosity.WITH_CLASS_INFO in verbose:
        # Set a flag in kwargs to temporarily store -cls.
        kwargs_['_store_cls'] = True
    result = default_dict_serializer(
        obj_dict,
        cls,
        key_transformer=key_transformer,
        strip_nulls=strip_nulls,
        strip_privates=strip_privates,
        strip_properties=strip_properties,
        strip_class_variables=strip_class_variables,
        strip_attr=strip_attr,
        **kwargs_)
    cls_name = get_class_name(cls, fully_qualified=True,
                              fork_inst=kwargs['fork_inst'])
    if not kwargs.get('_store_cls'):
        result = _get_dict_with_meta(result, cls_name, verbose,
                                     kwargs['fork_inst'])
    return result


def _get_dict_from_obj(
        obj,
        cls=None,
        strip_privates=False,
        strip_properties=False,
        strip_class_variables=False,
        strip_attr=False,
        *_,
        **__) -> dict:
    strip_attr = tuple(strip_attr) + _ABC_ATTRS
    excluded_elems = dir(JsonSerializable)
    props, other_cls_vars = _get_class_props(obj.__class__)
    # Make sure to get the slots of cls, not of any parent:
    slots = cls.__slots__ if '__slots__' in cls.__dict__ else {}
    return {attr: obj.__getattribute__(attr) for attr in dir(obj)
            if not attr.startswith('__')
            and not (strip_privates and attr.startswith('_'))
            and not (strip_properties and attr in props)
            and not (strip_class_variables and attr in other_cls_vars)
            and attr not in strip_attr
            and attr != 'json'
            and not isinstance(obj.__getattribute__(attr), Callable)
            and (not slots or attr in slots)
            and attr not in excluded_elems}


def _get_class_props(cls):
    props = []
    other_cls_vars = []
    for n, v in _get_complete_class_dict(cls).items():
        list_to_append = props if isinstance(v, property) else other_cls_vars
        list_to_append.append(n)
    return props, other_cls_vars


def _get_complete_class_dict(cls):
    cls_dict = {}
    # Loop reversed so values of sub-classes override those of super-classes.
    for cls_or_elder in reversed(cls.mro()):
        cls_dict.update(cls_or_elder.__dict__)
    return cls_dict


def _get_dict_with_meta(
        obj: dict,
        cls_name: str,
        verbose: Verbosity,
        fork_inst: type) -> dict:
    # This function will add a -meta section to the given obj (provided that
    # the given obj has -cls attributes for all children).
    if verbose is Verbosity.WITH_NOTHING:
        return obj

    obj[META_ATTR] = {}
    if Verbosity.WITH_CLASS_INFO in verbose:
        collection_of_types = {}
        _fill_collection_of_types(obj, cls_name, '/', collection_of_types)
        collection_of_types['/'] = cls_name
        obj[META_ATTR]['classes'] = collection_of_types
    if Verbosity.WITH_DUMP_TIME in verbose:
        dump_time = to_str(datetime.now(tz=timezone.utc), True, fork_inst)
        obj[META_ATTR]['dump_time'] = dump_time
    return obj


def _fill_collection_of_types(
        obj_: dict,
        cls_name_: Optional[str],
        prefix: str,
        collection_of_types_: dict) -> str:
    # This function loops through obj_ to fill collection_of_types_ with the
    # class names. All of the -cls attributes are removed in the process.
    cls_name_ = _get_class_name_and_strip_cls(cls_name_, obj_)
    for attr in obj_:
        if attr != META_ATTR and isinstance(obj_[attr], dict):
            attr_class = _fill_collection_of_types(obj_[attr],
                                                   None,
                                                   prefix + attr + '/',
                                                   collection_of_types_)
            collection_of_types_[prefix + attr] = attr_class
    return cls_name_


def _get_class_name_and_strip_cls(cls_name: Optional[str], obj: dict) -> str:
    result = cls_name
    if not cls_name and '-cls' in obj:
        result = obj['-cls']
    if '-cls' in obj:
        del obj['-cls']
    return result


_ABC_ATTRS = ('_abc_registry', '_abc_cache', '_abc_negative_cache',
              '_abc_negative_cache_version', '_abc_impl')
