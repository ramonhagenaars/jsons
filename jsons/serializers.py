"""
This module contains default serializers. You can override the serialization
process of a particular type as follows:

``jsons.set_serializer(custom_deserializer, SomeClass)``
"""
from datetime import datetime, time, timedelta, timezone
from enum import EnumMeta
from time import gmtime
from typing import Callable
from jsons import _common_impl
from jsons._common_impl import RFC3339_DATETIME_PATTERN, snakecase, \
    camelcase, pascalcase, lispcase, JsonSerializable


def default_iterable_serializer(obj, **kwargs) -> list:
    """
    Serialize the given ``obj`` to a list of serialized objects.
    :param obj: the iterable that is to be serialized.
    :param kwargs: any keyword arguments that may be given to the serialization
    process.
    :return: a list of which all elements are serialized.
    """
    return [_common_impl.dump(elem, **kwargs) for elem in obj]


def default_list_serializer(obj: list, **kwargs) -> list:
    """
    Serialize the given ``obj`` to a list of serialized objects.
    :param obj: the list that is to be serialized.
    :param kwargs: any keyword arguments that may be given to the serialization
    process.
    :return: a list of which all elements are serialized.
    """
    return default_iterable_serializer(obj, **kwargs)


def default_tuple_serializer(obj: tuple, **kwargs) -> list:
    """
    Serialize the given ``obj`` to a list of serialized objects.
    :param obj: the tuple that is to be serialized.
    :param kwargs: any keyword arguments that may be given to the serialization
    process.
    :return: a list of which all elements are serialized.
    """
    return default_iterable_serializer(obj, **kwargs)


def default_dict_serializer(obj: dict, strip_nulls: bool = False,
                            key_transformer: Callable[[str], str] = None,
                            **kwargs) -> dict:
    """
    Serialize the given ``obj`` to a dict of serialized objects.
    :param obj: the dict that is to be serialized.
    :param key_transformer: a function that will be applied to all keys in the
    resulting dict.
    :param strip_nulls: if ``True`` the resulting dict will not contain null
    values.
    :param kwargs: any keyword arguments that may be given to the serialization
    process.
    :return: a dict of which all elements are serialized.
    """
    result = dict()
    for key in obj:
        dumped_elem = _common_impl.dump(obj[key],
                                        key_transformer=key_transformer,
                                        strip_nulls=strip_nulls, **kwargs)
        if not (strip_nulls and dumped_elem is None):
            if key_transformer:
                key = key_transformer(key)
            result[key] = dumped_elem
    return result


def default_enum_serializer(obj: EnumMeta, use_enum_name: bool = True,
                            **_) -> str:
    """
    Serialize the given obj. By default, the name of the enum element is
    returned.
    :param obj: an instance of an enum.
    :param use_enum_name: determines whether the name or the value should be
    used for serialization.
    :param _: not used.
    :return: ``obj`` serialized as a string.
    """
    attr = 'name' if use_enum_name else 'value'
    return getattr(obj, attr)


def default_datetime_serializer(obj: datetime, strip_microseconds: bool = True,
                                **_) -> str:
    """
    Serialize the given datetime instance to a string. It uses the RFC3339
    pattern. If datetime is a localtime, an offset is provided. If datetime is
    in UTC, the result is suffixed with a 'Z'.
    :param obj: the datetime instance that is to be serialized.
    :param strip_microseconds: determines whether microseconds should be
    omitted.
    :param _: not used.
    :return: ``datetime`` as an RFC3339 string.
    """
    pattern = RFC3339_DATETIME_PATTERN
    offset = None
    tzone = obj.tzinfo
    if not tzone:
        hrs_delta = datetime.now().hour - gmtime().tm_hour
        if hrs_delta == 0:
            offset = '+00:00'
        else:
            tzone = timezone(timedelta(hours=hrs_delta))
    offset = offset or _datetime_offset(tzone)
    if not strip_microseconds and obj.microsecond:
        pattern += '.%f'
    return obj.strftime("{}{}".format(pattern, offset))


def _datetime_offset(tzone: timezone) -> str:
    offset = 'Z'
    if tzone.tzname(None) not in ('UTC', 'UTC+00:00'):
        tdelta = tzone.utcoffset(None)
        if not tdelta:
            tdelta = tzone.adjusted_offset
        offset_s = tdelta.total_seconds()
        offset_h = int(offset_s / 3600)
        offset_m = int((offset_s / 60) % 60)
        offset_t = time(abs(offset_h), abs(offset_m))
        operator = '+' if offset_s > 0 else '-'
        offset = offset_t.strftime('{}%H:%M'.format(operator))
    return offset


def default_primitive_serializer(obj, **_) -> object:
    """
    Serialize a primitive; simply return the given ``obj``.
    :param obj:
    :param _: not used.
    :return: ``obj``.
    """
    return obj


def default_object_serializer(obj: object,
                              key_transformer: Callable[[str], str] = None,
                              strip_nulls: bool = False,
                              strip_privates: bool = False,
                              strip_properties: bool = False,
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
    :param kwargs: any keyword arguments that are to be passed to the
    serializer functions.
    :return: a Python dict holding the values of ``obj``.
    """
    obj_dict = obj.__dict__ if strip_properties and hasattr(obj, '__dict__') \
        else _get_dict_from_obj(obj, strip_privates, **kwargs)
    return default_dict_serializer(obj_dict, key_transformer=key_transformer,
                                   strip_nulls=strip_nulls,
                                   strip_privates=strip_privates, **kwargs)


def _get_dict_from_obj(obj, strip_privates, cls=None, *_, **__):
    excluded_elems = dir(JsonSerializable)
    return {attr: obj.__getattribute__(attr) for attr in dir(obj)
            if not attr.startswith('__')
            and not (strip_privates and attr.startswith('_'))
            and attr != 'json'
            and not isinstance(obj.__getattribute__(attr), Callable)
            and (not cls or attr in cls.__slots__)
            and attr not in excluded_elems}


# The following default key transformers can be used with the
# default_object_serializer and default_dict_serializer.
KEY_TRANSFORMER_SNAKECASE = snakecase
KEY_TRANSFORMER_CAMELCASE = camelcase
KEY_TRANSFORMER_PASCALCASE = pascalcase
KEY_TRANSFORMER_LISPCASE = lispcase
