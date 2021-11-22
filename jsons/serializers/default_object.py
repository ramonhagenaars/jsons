import inspect
from datetime import datetime, timezone
from inspect import isfunction
from typing import Optional, Callable, Union, MutableSequence, Tuple, Dict

from typish import get_type, get_mro

from jsons import get_serializer, announce_class
from jsons._cache import cached
from jsons._common_impl import get_class_name, META_ATTR, StateHolder
from jsons._compatibility_impl import get_type_hints
from jsons._datetime_impl import to_str
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
        strict: bool = False,
        fork_inst: Optional[type] = StateHolder,
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
    :param verbose: if ``True`` the resulting dict will contain meta
    information (e.g. on how to deserialize).
    :param strict: a bool to determine if the serializer should be strict
    (i.e. only dumping stuff that is known to ``cls``).
    :param fork_inst: if given, it uses this fork of ``JsonSerializable``.
    :param kwargs: any keyword arguments that are to be passed to the
    serializer functions.
    :return: a Python dict holding the values
    of ``obj``.
    """
    strip_attr = _normalize_strip_attr(strip_attr)
    if cls and strict:
        attributes = _get_attributes_from_class(
            cls, strip_privates, strip_properties, strip_class_variables,
            strip_attr, strict)
    else:
        attributes = _get_attributes_from_object(
            obj, strip_privates, strip_properties, strip_class_variables,
            strip_attr, strict)
        cls = obj.__class__

    verbose = Verbosity.from_value(verbose)
    kwargs_ = {
        **kwargs,
        'fork_inst': fork_inst,
        'verbose': verbose,
        'strict': strict,
        # Set a flag in kwargs to temporarily store -cls:
        '_store_cls': Verbosity.WITH_CLASS_INFO in verbose
    }

    result = _do_serialize(obj=obj,
                           cls=cls,
                           attributes=attributes,
                           kwargs=kwargs_,
                           key_transformer=key_transformer,
                           strip_nulls=strip_nulls,
                           strip_privates=strip_privates,
                           strip_properties=strip_properties,
                           strip_class_variables=strip_class_variables,
                           strip_attr=strip_attr,
                           strict=strict,
                           fork_inst=fork_inst)

    cls_name = get_class_name(cls, fully_qualified=True)
    if not kwargs.get('_store_cls'):
        result = _get_dict_with_meta(result, cls_name, verbose, fork_inst)
    return result


def _do_serialize(
        obj: object,
        cls: type,
        attributes: Dict[str, Optional[type]],
        kwargs: dict,
        key_transformer: Optional[Callable[[str], str]] = None,
        strip_nulls: bool = False,
        strip_privates: bool = False,
        strip_properties: bool = False,
        strip_class_variables: bool = False,
        strip_attr: Union[str, MutableSequence[str], Tuple[str]] = None,
        strict: bool = False,
        fork_inst: Optional[type] = StateHolder) -> Dict[str, object]:
    result = dict()
    is_attrs_cls = getattr(cls, '__attrs_attrs__', None) is not None
    make_attributes_public = is_attrs_cls and not strip_privates
    for attr_name, cls_ in attributes.items():
        attr = getattr(obj, attr_name)
        attr_type = cls_ or type(attr)
        announce_class(attr_type, fork_inst=fork_inst)
        serializer = get_serializer(attr_type, fork_inst)
        try:
            dumped_elem = serializer(attr,
                                     cls=cls_,
                                     key_transformer=key_transformer,
                                     strip_nulls=strip_nulls,
                                     strip_privates=strip_privates,
                                     strip_properties=strip_properties,
                                     strip_class_variables=strip_class_variables,
                                     strip_attr=strip_attr,
                                     **kwargs)
            _store_cls_info(dumped_elem, attr, kwargs)
        except Exception as err:
            if strict:
                raise SerializationError(message=err.args[0]) from err
            else:
                fork_inst._warn('Failed to dump attribute "{}" of object of '
                                'type "{}". Reason: {}. Ignoring the '
                                'attribute.'
                                .format(attr, get_class_name(cls), err.args[0]),
                                'attribute-not-serialized')
                break

        if make_attributes_public:
            attr_name = attr_name.lstrip('_')
        _add_dumped_elem(result, attr_name, dumped_elem,
                         strip_nulls, key_transformer)
    return result


def _add_dumped_elem(
        result: dict,
        attr_name: str,
        dumped_elem: object,
        strip_nulls: bool,
        key_transformer: Optional[Callable[[str], str]]):
    if not (strip_nulls and dumped_elem is None):
        if key_transformer:
            attr_name = key_transformer(attr_name)
        result[attr_name] = dumped_elem


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
        strip_attr: tuple,
        strict: bool) -> Dict[str, Optional[type]]:
    # Get the attributes that are known in the class.
    attributes_and_types = _get_attributes_and_types(cls, strict)
    return _filter_attributes(cls, attributes_and_types, strip_privates,
                              strip_properties, strip_class_variables,
                              strip_attr)


def _get_attributes_from_object(
        obj: object,
        strip_privates: bool,
        strip_properties: bool,
        strip_class_variables: bool,
        strip_attr: tuple,
        strict: bool) -> Dict[str, Optional[type]]:
    # Get the attributes that are known in the object.
    cls = obj.__class__
    attributes_and_types = _get_attributes_and_types(cls, strict)
    attributes = {attr: attributes_and_types.get(attr, None)
                  for attr in dir(obj)}
    return _filter_attributes(cls, attributes, strip_privates,
                              strip_properties, strip_class_variables,
                              strip_attr)


@cached
def _get_attributes_and_types(cls: type,
                              strict: bool) -> Dict[str, Optional[type]]:
    if '__slots__' in cls.__dict__:
        attributes = {attr: None for attr in cls.__slots__}
    elif hasattr(cls, '__annotations__'):
        attributes = get_type_hints(cls)
    elif strict:
        hints = get_type_hints(cls.__init__)
        attributes = {k: hints[k] for k in hints if k != 'self'}
    else:
        attributes = {}

    # Add properties and class variables.
    props, class_vars = _get_class_props(cls)
    for elem in props + class_vars:
        attributes[elem] = None

    return attributes


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
            and not inspect.ismethod(getattr(cls, attr, None))
            and not isfunction(getattr(cls, attr, None))
            and attr not in excluded_elems
            and not _is_innerclass(attr, cls)}


@cached
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
    for cls_or_elder in reversed(get_mro(cls)):
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


def _store_cls_info(result: object, original_obj: dict, kwargs):
    if kwargs.get('_store_cls', None) and isinstance(result, dict):
        cls = get_type(original_obj)
        if cls.__module__ == 'typing':
            cls_name = repr(cls)
        else:
            cls_name = get_class_name(cls, fully_qualified=True)
        result['-cls'] = cls_name


@cached
def _is_innerclass(attr: str, cls: type) -> bool:
    attr_obj = getattr(cls, attr, None)
    return (isinstance(attr_obj, type)
            and inspect.getsource(attr_obj) in inspect.getsource(cls))


_ABC_ATTRS = ('_abc_registry', '_abc_cache', '_abc_negative_cache',
              '_abc_negative_cache_version', '_abc_impl')
