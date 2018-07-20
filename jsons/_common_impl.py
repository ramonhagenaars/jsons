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


def dump_impl(obj: object, **kwargs) -> dict:
    """
    Serialize the given ``obj`` to a dict.

    The way objects are serialized can be finetuned by setting serializer
    functions for the specific type using ``set_serializer``.
    :param obj: a Python instance of any sort.
    :param kwargs: the keyword args are passed on to the serializer function.
    :return: the serialized obj as a dict.
    """
    serializer = SERIALIZERS.get(obj.__class__.__name__, None)
    if not serializer:
        parents = [cls for cls in CLASSES_SERIALIZERS if isinstance(obj, cls)]
        if parents:
            serializer = SERIALIZERS[parents[0].__name__]
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
    :param kwargs: the keyword args are passed on to the deserializer function.
    :return: an instance of ``cls`` if given, a dict otherwise.
    """
    cls = cls or type(json_obj)
    cls_name = cls.__name__ if hasattr(cls, '__name__') \
        else cls.__origin__.__name__
    deserializer = DESERIALIZERS.get(cls_name, None)
    if not deserializer:
        parents = [cls_ for cls_ in CLASSES_DESERIALIZERS
                   if issubclass(cls, cls_)]
        if parents:
            deserializer = DESERIALIZERS[parents[0].__name__]
    return deserializer(json_obj, cls, **kwargs)


def camelcase(s: str) -> str:
    """
    Return `s` in camelCase.
    :param s: the string that is to be transformed.
    :return: a string in camelCase.
    """
    s = s.replace('-', '_')
    splitted = s.split('_')
    if len(splitted) > 1:
        s = ''.join([x.title() for x in splitted])
    return s[0].lower() + s[1:]


def snakecase(s: str) -> str:
    """
    Return `s` in snake_case.
    :param s: the string that is to be transformed.
    :return: a string in snake_case.
    """
    s = s.replace('-', '_')
    s = s[0].lower() + s[1:]
    return re.sub(r'([a-z])([A-Z])', '\\1_\\2', s).lower()


def pascalcase(s: str) -> str:
    """
    Return `s` in PascalCase.
    :param s: the string that is to be transformed.
    :return: a string in PascalCase.
    """
    camelcase_str = camelcase(s)
    return camelcase_str[0].upper() + camelcase_str[1:]


def lispcase(s: str) -> str:
    """
    Return `s` in lisp-case.
    :param s: the string that is to be transformed.
    :return: a string in lisp-case.
    """
    return snakecase(s).replace('_', '-')
