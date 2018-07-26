"""
This module contains common implementation details of jsons. This module is
private, do not import (from) it directly.
"""
import re

JSON_TYPES = (str, int, float, bool)
RFC3339_DATETIME_PATTERN = '%Y-%m-%dT%H:%M:%S'
CLASSES_SERIALIZERS = list()
CLASSES_DESERIALIZERS = list()
SERIALIZERS = dict()
DESERIALIZERS = dict()


def dump_impl(obj: object, **kwargs) -> object:
    """
    Serialize the given ``obj`` to a JSON equivalent type (e.g. dict, list,
    int, ...).

    The way objects are serialized can be finetuned by setting serializer
    functions for the specific type using ``set_serializer``.
    :param obj: a Python instance of any sort.
    :param kwargs: the keyword args are passed on to the serializer function.
    :return: the serialized obj as a JSON type.
    """
    serializer = SERIALIZERS.get(obj.__class__.__name__.lower(), None)
    if not serializer:
        parents = [cls for cls in CLASSES_SERIALIZERS if isinstance(obj, cls)]
        if parents:
            serializer = SERIALIZERS[parents[0].__name__.lower()]
    return serializer(obj, **kwargs)


def load_impl(json_obj: dict, cls: type = None, **kwargs) -> object:
    """
    Deserialize the given ``json_obj`` to an object of type ``cls``. If the
    contents of ``json_obj`` do not match the interface of ``cls``, a
    TypeError is raised.

    If ``json_obj`` contains a value that belongs to a custom class, there must
    be a type hint present for that value in ``cls`` to let this function know
    what type it should deserialize that value to.


    **Example**:

    >>> from typing import List
    >>> import jsons
    >>> class Person:
    ...     # No type hint required for name
    ...     def __init__(self, name):
    ...         self.name = name
    >>> class Family:
    ...     # Person is a custom class, use a type hint
    ...         def __init__(self, persons: List[Person]):
    ...             self.persons = persons
    >>> loaded = jsons.load({'persons': [{'name': 'John'}]}, Family)
    >>> loaded.persons[0].name
    'John'

    If no ``cls`` is given, a dict is simply returned, but contained values
    (e.g. serialized ``datetime`` values) are still deserialized.
    :param json_obj: the dict that is to be deserialized.
    :param cls: a matching class of which an instance should be returned.
    :param kwargs: the keyword args are passed on to the deserializer function.
    :return: an instance of ``cls`` if given, a dict otherwise.
    """
    cls = cls or type(json_obj)
    cls_name = cls.__name__ if hasattr(cls, '__name__') \
        else cls.__origin__.__name__
    deserializer = DESERIALIZERS.get(cls_name.lower(), None)
    if not deserializer:
        parents = [cls_ for cls_ in CLASSES_DESERIALIZERS
                   if issubclass(cls, cls_)]
        if parents:
            deserializer = DESERIALIZERS[parents[0].__name__.lower()]
    return deserializer(json_obj, cls, **kwargs)


def camelcase(str_: str) -> str:
    """
    Return ``s`` in camelCase.
    :param str_: the string that is to be transformed.
    :return: a string in camelCase.
    """
    str_ = str_.replace('-', '_')
    splitted = str_.split('_')
    if len(splitted) > 1:
        str_ = ''.join([x.title() for x in splitted])
    return str_[0].lower() + str_[1:]


def snakecase(str_: str) -> str:
    """
    Return ``s`` in snake_case.
    :param str_: the string that is to be transformed.
    :return: a string in snake_case.
    """
    str_ = str_.replace('-', '_')
    str_ = str_[0].lower() + str_[1:]
    return re.sub(r'([a-z])([A-Z])', '\\1_\\2', str_).lower()


def pascalcase(str_: str) -> str:
    """
    Return ``s`` in PascalCase.
    :param str_: the string that is to be transformed.
    :return: a string in PascalCase.
    """
    camelcase_str = camelcase(str_)
    return camelcase_str[0].upper() + camelcase_str[1:]


def lispcase(str_: str) -> str:
    """
    Return ``s`` in lisp-case.
    :param str_: the string that is to be transformed.
    :return: a string in lisp-case.
    """
    return snakecase(str_).replace('_', '-')
