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
    """
    Serialize the given ``obj`` to a dict.

    The way objects are serialized can be finetuned by setting serializer
    functions for the specific type using ``set_serializer``.
    :param obj: a Python instance of any sort.
    :return: the serialized obj as a dict.
    """
    serializer = _SERIALIZERS.get(obj.__class__.__name__, None)
    if not serializer:
        parents = [cls for cls in _CLASSES if isinstance(obj, cls)]
        if parents:
            serializer = _SERIALIZERS[parents[0].__name__]
    return serializer(obj)


def load(json_obj: dict, cls: type = None) -> object:
    """
    Deserialize the given ``json_obj`` to an object of type ``cls``. If the
    contents of ``json_obj`` do not match the interface of ``cls``, a
    TypeError is raised.

    If ``json_obj`` contains a value that belongs to a custom class, there must
    be a type hint present for that value in ``cls`` to let this function know
    what type it should deserialize that value to.


    **Example**:

        ``class Person:``
            ``# No type hint required for name``

        ``class Person:``
            ``# No type hint required for name``

            ``def __init__(self, name):``
                ``self.name = name``
        ````
        ``class Family:``
            ``# Person is a custom class, use a type hint``

            ``def __init__(self, persons: List[Person]):``
                ``self.persons = persons``

        ``jsons.load(some_dict, Family)``

    If no ``cls`` is given, a dict is simply returned, but contained values
    (e.g. serialized ``datetime`` values) are still deserialized.
    :param json_obj: the dict that is to be deserialized.
    :param cls: a matching class of which an instance should be returned.
    :return: an instance of ``cls`` if given, a dict otherwise.
    """
    cls = cls or type(json_obj)
    cls_name = cls.__name__ if hasattr(cls, '__name__') \
        else cls.__origin__.__name__
    deserializer = _DESERIALIZERS.get(cls_name, None)
    if not deserializer:
        parents = [cls_ for cls_ in _CLASSES if issubclass(cls, cls_)]
        if parents:
            deserializer = _DESERIALIZERS[parents[0].__name__]
    return deserializer(json_obj, cls)


def dumps(obj: object, *args, **kwargs) -> str:
    """
    Extend ``json.dumps``, allowing any Python instance to be dumped to a
    string. Any extra (keyword) arguments are passed on to ``json.dumps``.

    :param obj: the object that is to be dumped to a string.
    :param args: extra arguments for ``json.dumps``.
    :param kwargs: extra keyword arguments for ``json.dumps``.
    :return: ``obj`` as a ``str``.
    """
    return json.dumps(dump(obj), *args, **kwargs)


def loads(s: str, cls: type = None, *args, **kwargs) -> object:
    """
    Extend ``json.loads``, allowing a string to be loaded into a dict or a
    Python instance of type ``cls``. Any extra (keyword) arguments are passed
    on to ``json.loads``.

    :param s: the string that is to be loaded.
    :param cls: a matching class of which an instance should be returned.
    :param args: extra arguments for ``json.dumps``.
    :param kwargs: extra keyword arguments for ``json.dumps``.
    :return: an instance of type ``cls`` or a dict if no ``cls`` is given.
    """
    obj = json.loads(s, *args, **kwargs)
    return load(obj, cls) if cls else obj


def set_serializer(c: callable, cls: type) -> None:
    """
    Set a serializer function for the given type. You may override the default
    behavior of ``jsons.load`` by setting a custom serializer.

    :param c: the serializer function.
    :param cls: the type this serializer can handle.
    :return: None.
    """
    if cls:
        _CLASSES.insert(0, cls)
        _SERIALIZERS[cls.__name__] = c
    else:
        _SERIALIZERS['NoneType'] = c


def set_deserializer(c: callable, cls: type) -> None:
    """
    Set a deserializer function for the given type. You may override the
    default behavior of ``jsons.dump`` by setting a custom deserializer.

    :param c: the deserializer function.
    :param cls: the type this serializer can handle.
    :return: None.
    """
    if cls:
        _CLASSES.insert(0, cls)
        _DESERIALIZERS[cls.__name__] = c
    else:
        _DESERIALIZERS['NoneType'] = c


class JsonSerializable:
    """
    This class offers an alternative to using the `jsons.load` and `jsons.dump`
    methods. An instance of a class that inherits from JsonSerializable has the
    `json` property, which value is equivalent to calling `jsons.dump` on that
    instance. Furthermore, you can call `from_json` on that class, which is
    equivalent to calling `json.load` with that class as an argument.
    """
    @property
    def json(self) -> dict:
        """
        See `jsons.dump`.
        :return: this instance in a JSON representation (dict).
        """
        return dump(self)

    @classmethod
    def from_json(cls, json_obj: dict) -> object:
        """
        See `jsons.load`.
        :param json_obj: a JSON representation of an instance of the inheriting
        class
        :return: an instance of the inheriting class.
        """
        return load(json_obj, cls)


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
    pattern = _RFC3339_DATETIME_PATTERN
    if timezone:
        if timezone.tzname(None) != 'UTC':
            offset = timezone.tzname(None).split('UTC')[1]
    if obj.microsecond:
        pattern += '.%f'
    return obj.strftime("{}{}".format(pattern, offset))


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
        dattim_str = obj[0:-1]
        dattim_obj = datetime.strptime(dattim_str, pattern)
    else:
        dattim_str, offset = obj.split('+')
        dattim_obj = datetime.strptime(dattim_str, pattern)
        hours, minutes = offset.split(':')
        tz = timezone(offset=timedelta(hours=int(hours), minutes=int(minutes)))
        datetime_list = [dattim_obj.year, dattim_obj.month, dattim_obj.day,
                         dattim_obj.hour, dattim_obj.minute, dattim_obj.second,
                         dattim_obj.microsecond, tz]
        dattim_obj = datetime(*datetime_list)
    return dattim_obj


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
        loaded_attr = load(remaining_attrs[attr_name],
                           type(remaining_attrs[attr_name]))
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
