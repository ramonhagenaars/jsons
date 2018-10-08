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
from datetime import datetime
from enum import Enum
from jsons import _common_impl
from jsons.deserializers import default_list_deserializer, \
    default_enum_deserializer, default_datetime_deserializer, \
    default_string_deserializer, default_primitive_deserializer, \
    default_object_deserializer, default_dict_deserializer, \
    default_tuple_deserializer, default_set_deserializer
from jsons.serializers import default_list_serializer, \
    default_enum_serializer, default_datetime_serializer, \
    default_primitive_serializer, default_object_serializer, \
    KEY_TRANSFORMER_SNAKECASE, KEY_TRANSFORMER_CAMELCASE, \
    KEY_TRANSFORMER_PASCALCASE, KEY_TRANSFORMER_LISPCASE, \
    default_dict_serializer, default_tuple_serializer

dump = _common_impl.dump
load = _common_impl.load
dumps = _common_impl.dumps
loads = _common_impl.loads
dumpb = _common_impl.dumpb
loadb = _common_impl.loadb
JsonSerializable = _common_impl.JsonSerializable
set_serializer = _common_impl.set_serializer
set_deserializer = _common_impl.set_deserializer

set_serializer(default_list_serializer, list)
set_serializer(default_list_serializer, set)
set_serializer(default_tuple_serializer, tuple)
set_serializer(default_dict_serializer, dict)
set_serializer(default_enum_serializer, Enum)
set_serializer(default_datetime_serializer, datetime)
set_serializer(default_primitive_serializer, str)
set_serializer(default_primitive_serializer, int)
set_serializer(default_primitive_serializer, float)
set_serializer(default_primitive_serializer, bool)
set_serializer(default_primitive_serializer, None)
set_serializer(default_object_serializer, object, False)
set_deserializer(default_list_deserializer, list)
set_deserializer(default_tuple_deserializer, tuple)
set_deserializer(default_set_deserializer, set)
set_deserializer(default_dict_deserializer, dict)
set_deserializer(default_enum_deserializer, Enum)
set_deserializer(default_datetime_deserializer, datetime)
set_deserializer(default_string_deserializer, str)
set_deserializer(default_primitive_deserializer, int)
set_deserializer(default_primitive_deserializer, float)
set_deserializer(default_primitive_deserializer, bool)
set_deserializer(default_primitive_deserializer, None)
set_deserializer(default_object_deserializer, object, False)
