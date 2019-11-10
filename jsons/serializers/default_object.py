from datetime import datetime, timezone
from inspect import isfunction
from typing import Optional, Callable, Union, MutableSequence, Tuple, Dict

from jsons._cache import cached
from jsons._common_impl import get_class_name, META_ATTR
from jsons._datetime_impl import to_str
from jsons._dump_impl import dump
from jsons.classes import JsonSerializable
from jsons.classes.verbosity import Verbosity
from jsons.exceptions import SerializationError


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
        **kwargs) -> Optional[dict]:
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

    _check_slots(cls, kwargs)
    strip_attr = _normalize_strip_attr(strip_attr)

    if cls:
        attributes = _get_attributes_from_class(
            cls, strip_privates, strip_properties, strip_class_variables,
            strip_attr)
    else:
        attributes = _get_attributes_from_object(
            obj, strip_privates, strip_properties, strip_class_variables,
            strip_attr)
        cls = obj.__class__

    kwargs_ = {**kwargs, 'verbose': verbose}
    verbose = Verbosity.from_value(verbose)
    if Verbosity.WITH_CLASS_INFO in verbose:
        # Set a flag in kwargs to temporarily store -cls.
        kwargs_['_store_cls'] = True

    obj_dict = {attr: obj.__getattribute__(attr) for attr in attributes}
    result = dump(obj_dict, cls=dict, key_transformer=key_transformer,
                  strip_nulls=strip_nulls, strip_privates=strip_privates,
                  strip_properties=strip_properties,
                  strip_class_variables=strip_class_variables,
                  strip_attr=strip_attr, types=attributes, **kwargs_)

    cls_name = get_class_name(cls, fully_qualified=True,
                              fork_inst=kwargs['fork_inst'])
    if not kwargs.get('_store_cls'):
        result = _get_dict_with_meta(result, cls_name, verbose,
                                     kwargs['fork_inst'])
    return result


def _check_slots(cls: type, kwargs):
    # Check for __slots__ or __dataclass_fields__.
    if (cls and not hasattr(cls, '__slots__')
            and not hasattr(cls, '__dataclass_fields__')):
        raise SerializationError('Invalid type: "{}". Only dataclasses or '
                                 'types that have a __slots__ defined are '
                                 'allowed when providing "cls".'
                                 .format(get_class_name(cls, fork_inst=kwargs['fork_inst'], fully_qualified=True)))


def _normalize_strip_attr(strip_attr) -> tuple:
    # Make sure that strip_attr is always a tuple.
    strip_attr = strip_attr or tuple()
    if (not isinstance(strip_attr, MutableSequence)
            and not isinstance(strip_attr, tuple)):
        strip_attr = (strip_attr,)
    return strip_attr


@cached
def _get_attributes_from_class(
        cls: type,
        strip_privates: bool,
        strip_properties: bool,
        strip_class_variables: bool,
        strip_attr: tuple) -> Dict[str, Optional[type]]:
    # Get the attributes that are known in the class.
    if '__slots__' in cls.__dict__:
        attributes = {attr: None for attr in cls.__slots__}
    elif hasattr(cls, '__annotations__'):
        attributes = cls.__annotations__
    else:
        attributes = {}
    return _filter_attributes(cls, attributes, strip_privates,
                              strip_properties, strip_class_variables,
                              strip_attr)


def _get_attributes_from_object(
        obj: object,
        strip_privates: bool,
        strip_properties: bool,
        strip_class_variables: bool,
        strip_attr: tuple) -> Dict[str, Optional[type]]:
    # Get the attributes that are known in the object.
    attributes = {attr: None for attr in dir(obj)}
    # TODO maybe check if we can still get the types of these attributes
    cls = obj.__class__
    return _filter_attributes(cls, attributes, strip_privates,
                              strip_properties, strip_class_variables,
                              strip_attr)


def _filter_attributes(
        cls: type,
        attributes: Dict[str, Optional[type]],
        strip_privates: bool,
        strip_properties: bool,
        strip_class_variables: bool,
        strip_attr: tuple) -> Dict[str, Optional[type]]:
    # Filter the given attributes with the given preferences.
    strip_attr = strip_attr + _ABC_ATTRS
    excluded_elems = dir(JsonSerializable)
    props, other_cls_vars = _get_class_props(cls)

    return {attr: type_ for attr, type_ in attributes.items()
            if not attr.startswith('__')
            and not (strip_privates and attr.startswith('_'))
            and not (strip_properties and attr in props)
            and not (strip_class_variables and attr in other_cls_vars)
            and attr not in strip_attr
            and attr != 'json'
            and not isfunction(getattr(cls, attr, None))
            and attr not in excluded_elems}


    # return [(attr, type_) for attr, type_ in attributes.items()
    #         if not attr.startswith('__')
    #         and not (strip_privates and attr.startswith('_'))
    #         and not (strip_properties and attr in props)
    #         and not (strip_class_variables and attr in other_cls_vars)
    #         and attr not in strip_attr
    #         and attr != 'json'
    #         and not isfunction(getattr(cls, attr, None))
    #         and attr not in excluded_elems]


def _get_class_props(cls: type) -> Tuple[list, list]:
    props = []
    other_cls_vars = []
    for n, v in _get_complete_class_dict(cls).items():
        list_to_append = props if isinstance(v, property) else other_cls_vars
        list_to_append.append(n)
    return props, other_cls_vars


def _get_complete_class_dict(cls: type) -> dict:
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
