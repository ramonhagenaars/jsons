"""
Works with Python3.5+

JSON (de)serialization (jsons) from and to dicts and plain old Python objects.

Works with dataclasses (Python3.7+).


**Example:**

    >>> from dataclasses import dataclass
    >>> @dataclass
    ... class Car:
    ...     color: str
    >>> @dataclass
    ... class Person:
    ...     car: Car
    ...     name: str
    >>> c = Car('Red')
    >>> p = Person(c, 'John')
    >>> dumped = dump(p)
    >>> dumped['name']
    'John'
    >>> dumped['car']['color']
    'Red'
    >>> p_reloaded = load(dumped, Person)
    >>> p_reloaded.name
    'John'
    >>> p_reloaded.car.color
    'Red'


Deserialization will work with older Python classes (Python3.5+) given that
type hints are present for custom types (i.e. any type that is not set at
the bottom of this module). Serialization will work with no type hints at
all.


**Example**

    >>> class Car:
    ...     def __init__(self, color):
    ...         self.color = color
    >>> class Person:
    ...     def __init__(self, car: Car, name):
    ...         self.car = car
    ...         self.name = name
    >>> c = Car('Red')
    >>> p = Person(c, 'John')
    >>> dumped = dump(p)
    >>> dumped['name']
    'John'
    >>> dumped['car']['color']
    'Red'
    >>> p_reloaded = load(dumped, Person)
    >>> p_reloaded.name
    'John'
    >>> p_reloaded.car.color
    'Red'


Alternatively, you can make use of the `JsonSerializable` class.


**Example**

    >>> class Car(JsonSerializable):
    ...     def __init__(self, color):
    ...         self.color = color
    >>> class Person(JsonSerializable):
    ...     def __init__(self, car: Car, name):
    ...         self.car = car
    ...         self.name = name
    >>> c = Car('Red')
    >>> p = Person(c, 'John')
    >>> dumped = p.json
    >>> dumped['name']
    'John'
    >>> dumped['car']['color']
    'Red'
    >>> p_reloaded = Person.from_json(dumped)
    >>> p_reloaded.name
    'John'
    >>> p_reloaded.car.color
    'Red'

"""
from collections.abc import Mapping
from datetime import datetime, date, time, timezone, timedelta
from enum import Enum
from typing import Union, List, Tuple, Iterable
from uuid import UUID
from jsons._common_impl import NoneType
from jsons._key_transformers import snakecase, camelcase, pascalcase, lispcase
from jsons import (
    _dump_impl,
    _load_impl,
    _fork_impl,
    _lizers_impl,
    _validation,
    _extra_impl,
    deserializers,
    serializers,
    classes
)
from jsons.exceptions import (
    JsonsError,
    ValidationError,
    DeserializationError,
    DecodeError,
    UnfulfilledArgumentError,
    InvalidDecorationError
)


dump = _dump_impl.dump
dumps = _dump_impl.dumps
dumpb = _dump_impl.dumpb
load = _load_impl.load
loads = _load_impl.loads
loadb = _load_impl.loadb
fork = _fork_impl.fork
JsonSerializable = classes.JsonSerializable
set_serializer = _lizers_impl.set_serializer
get_serializer = _lizers_impl.get_serializer
set_deserializer = _lizers_impl.set_deserializer
get_deserializer = _lizers_impl.get_deserializer
get_validator = _validation.get_validator
set_validator = _validation.set_validator
validate = _validation.validate
announce_class = _extra_impl.announce_class
suppress_warnings = _extra_impl.suppress_warnings

KEY_TRANSFORMER_SNAKECASE = snakecase
KEY_TRANSFORMER_CAMELCASE = camelcase
KEY_TRANSFORMER_PASCALCASE = pascalcase
KEY_TRANSFORMER_LISPCASE = lispcase

Verbosity = classes.verbosity.Verbosity

# Redeclare the serializers and deserializers:
default_tuple_serializer = serializers.default_tuple_serializer
default_dict_serializer = serializers.default_dict_serializer
default_iterable_serializer = serializers.default_iterable_serializer
default_enum_serializer = serializers.default_enum_serializer
default_datetime_serializer = serializers.default_datetime_serializer
default_date_serializer = serializers.default_date_serializer
default_time_serializer = serializers.default_time_serializer
default_timezone_serializer = serializers.default_timezone_serializer
default_timedelta_serializer = serializers.default_timedelta_serializer
default_primitive_serializer = serializers.default_primitive_serializer
default_object_serializer = serializers.default_object_serializer
default_uuid_serializer = serializers.default_uuid_serializer

default_list_deserializer = deserializers.default_list_deserializer
default_tuple_deserializer = deserializers.default_tuple_deserializer
default_union_deserializer = deserializers.default_union_deserializer
default_dict_deserializer = deserializers.default_dict_deserializer
default_enum_deserializer = deserializers.default_enum_deserializer
default_datetime_deserializer = deserializers.default_datetime_deserializer
default_date_deserializer = deserializers.default_date_deserializer
default_time_deserializer = deserializers.default_time_deserializer
default_timezone_deserializer = deserializers.default_timezone_deserializer
default_timedelta_deserializer = deserializers.default_timedelta_deserializer
default_string_deserializer = deserializers.default_string_deserializer
default_nonetype_deserializer = deserializers.default_nonetype_deserializer
default_primitive_deserializer = deserializers.default_primitive_deserializer
default_mapping_deserializer = deserializers.default_mapping_deserializer
default_iterable_deserializer = deserializers.default_iterable_deserializer
default_object_deserializer = deserializers.default_object_deserializer
default_uuid_deserializer = deserializers.default_uuid_deserializer
default_complex_serializer = deserializers.default_complex_deserializer

# Set the serializers:
set_serializer(default_tuple_serializer, (tuple, Tuple))
set_serializer(default_enum_serializer, Enum)
set_serializer(default_datetime_serializer, datetime)
set_serializer(default_date_serializer, date)
set_serializer(default_time_serializer, time)
set_serializer(default_timezone_serializer, timezone)
set_serializer(default_timedelta_serializer, timedelta)
set_serializer(default_primitive_serializer, (str, int, float, bool, None))
set_serializer(default_dict_serializer, Mapping, False)
set_serializer(default_iterable_serializer, Iterable, False)
set_serializer(default_object_serializer, object, False)
set_serializer(default_uuid_serializer, UUID)

# Set the deserializers:
set_deserializer(default_list_deserializer, (list, List))
set_deserializer(default_tuple_deserializer, (tuple, Tuple))
set_deserializer(default_union_deserializer, Union)
set_deserializer(default_enum_deserializer, Enum)
set_deserializer(default_datetime_deserializer, datetime)
set_deserializer(default_date_deserializer, date)
set_deserializer(default_time_deserializer, time)
set_deserializer(default_timezone_deserializer, timezone)
set_deserializer(default_timedelta_deserializer, timedelta)
set_deserializer(default_string_deserializer, str)
set_deserializer(default_nonetype_deserializer, NoneType)
set_deserializer(default_primitive_deserializer, (int, float, bool))
set_deserializer(default_mapping_deserializer, Mapping, False)
set_deserializer(default_iterable_deserializer, Iterable, False)
set_deserializer(default_object_deserializer, object, False)
set_deserializer(default_uuid_deserializer, UUID)
set_deserializer(default_complex_serializer, complex)
