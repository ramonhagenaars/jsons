import inspect
import json
import re
from datetime import datetime, timedelta, timezone
from enum import Enum, EnumMeta
from typing import List

_JSON_TYPES = (str, int, float, bool)
_RFC3339_DATETIME_PATTERN = '%Y-%m-%dT%H:%M:%S'
_CLASSES = list()
_SERIALIZERS = dict()
_DESERIALIZERS = dict()


def dump(obj: object) -> dict:
    serializer = _SERIALIZERS.get(obj.__class__.__name__, None)
    if not serializer:
        parents = [cls for cls in _CLASSES if isinstance(obj, cls)]
        if parents:
            serializer = _SERIALIZERS[parents[0].__name__]
    return serializer(obj)


def load(json_obj: object, cls: type = None) -> object:
    cls = cls or type(json_obj)
    cls_name = cls.__name__ if hasattr(cls, '__name__') else cls.__origin__.__name__
    deserializer = _DESERIALIZERS.get(cls_name, None)
    if not deserializer:
        parents = [cls_ for cls_ in _CLASSES if issubclass(cls, cls_)]
        if parents:
            deserializer = _DESERIALIZERS[parents[0].__name__]
    return deserializer(json_obj, cls)


def dumps(obj: object) -> str:
    return json.dumps(dump(obj))


def loads(s: str, cls: type = None) -> object:
    obj = json.loads(s)
    return load(obj, cls) if cls else obj


def set_serializer(c: callable, cls: type) -> None:
    if cls:
        _CLASSES.insert(0, cls)
        _SERIALIZERS[cls.__name__] = c
    else:
        _SERIALIZERS['NoneType'] = c


def set_deserializer(c: callable, cls: type) -> None:
    if cls:
        _CLASSES.insert(0, cls)
        _DESERIALIZERS[cls.__name__] = c
    else:
        _DESERIALIZERS['NoneType'] = c


#######################
# Default serializers #
#######################

def _default_list_serializer(obj: list) -> dict:
    return [dump(elem) for elem in obj]


def _default_enum_serializer(obj: EnumMeta) -> dict:
    return obj.name


def _default_datetime_serializer(obj: datetime) -> dict:
    timezone = obj.tzinfo
    offset = 'Z'
    if timezone:
        if timezone.tzname(None) != 'UTC':
            offset = timezone.tzname(None).split('UTC')[1]
    return obj.strftime("{}{}".format(_RFC3339_DATETIME_PATTERN, offset))


def _default_primitive_serializer(obj) -> dict:
    return obj


def _default_object_serializer(obj) -> dict:
    d = obj.__dict__
    return {key: dump(d[key]) for key in d}


#########################
# Default deserializers #
#########################

def _default_datetime_deserializer(obj: str, _: datetime) -> datetime:
    pattern = _RFC3339_DATETIME_PATTERN
    if '.' in obj:
        pattern += '.%f'
        # strptime allows a fraction of length 6, so trip the rest (if exists).
        regex_pattern = re.compile('(\.[0-9]+)')
        frac = regex_pattern.search(obj).group()
        obj = obj.replace(frac, frac[0:7])
    if obj[-1] == 'Z':
        datetime_str = obj[0:-1]
        datetime_obj = datetime.strptime(datetime_str, pattern)
    else:
        datetime_str, offset = obj.split('+')
        datetime_obj = datetime.strptime(datetime_str, pattern)
        hours, minutes = offset.split(':')
        tz = timezone(offset=timedelta(hours=int(hours), minutes=int(minutes)))
        datetime_list = [datetime_obj.year, datetime_obj.month, datetime_obj.day,
                         datetime_obj.hour, datetime_obj.minute, datetime_obj.second,
                         datetime_obj.microsecond, tz]
        datetime_obj = datetime(*datetime_list)
    return datetime_obj


def _default_object_deserializer(obj: dict, cls: type) -> object:
    signature_parameters = inspect.signature(cls.__init__).parameters
    # Loop through the signature of cls: the type we try to deserialize to. For
    # every required parameter, we try to get the corresponding value from
    # json_obj.
    constructor_args = dict()
    for signature_key, signature in signature_parameters.items():
        if obj and signature_key is not 'self':
            if signature_key in obj:
                cls_ = None
                if signature.annotation != inspect._empty:
                    cls_ = signature.annotation
                value = load(obj[signature_key], cls_)
                constructor_args[signature_key] = value

    # The constructor arguments are gathered, create an instance.
    instance = cls(**constructor_args)
    # Set any remaining attributes on the newly created instance.
    remaining_attrs = {attr_name: obj[attr_name] for attr_name in obj
                       if attr_name not in constructor_args}
    for attr_name in remaining_attrs:
        loaded_attr = load(remaining_attrs[attr_name], type(remaining_attrs[attr_name]))
        setattr(instance, attr_name, loaded_attr)
    return instance


def _default_list_deserializer(obj: List, cls) -> object:
    cls_ = None
    if cls and hasattr(cls, '__args__'):
        cls_ = cls.__args__[0]
    return [load(x, cls_) for x in obj]


def _default_enum_deserializer(obj: Enum, cls: EnumMeta) -> object:
    return cls[obj]


def _default_string_deserializer(obj: str, _: type = None) -> object:
    try:
        return load(obj, datetime)
    except:
        return obj


def _default_primitive_deserializer(obj: object, _: type = None) -> object:
    return obj

# The order of the below is important.
set_serializer(_default_object_serializer, object)
set_serializer(_default_list_serializer, list)
set_serializer(_default_enum_serializer, Enum)
set_serializer(_default_datetime_serializer, datetime)
set_serializer(_default_primitive_serializer, str)
set_serializer(_default_primitive_serializer, int)
set_serializer(_default_primitive_serializer, float)
set_serializer(_default_primitive_serializer, bool)
set_serializer(_default_primitive_serializer, dict)
set_serializer(_default_primitive_serializer, None)
set_deserializer(_default_object_deserializer, object)
set_deserializer(_default_list_deserializer, list)
set_deserializer(_default_enum_deserializer, Enum)
set_deserializer(_default_datetime_deserializer, datetime)
set_deserializer(_default_string_deserializer, str)
set_deserializer(_default_primitive_deserializer, int)
set_deserializer(_default_primitive_deserializer, float)
set_deserializer(_default_primitive_deserializer, bool)
set_deserializer(_default_primitive_deserializer, dict)
set_deserializer(_default_primitive_deserializer, None)
