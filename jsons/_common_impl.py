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


def dump(obj: object, **kwargs) -> object:
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


def load(json_obj: dict, cls: type = None, **kwargs) -> object:
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

    If the type of `json_obj` exactly matches `cls` then `json_obj` is simply
    returned.

    :param json_obj: the dict that is to be deserialized.
    :param cls: a matching class of which an instance should be returned.
    :param kwargs: the keyword args are passed on to the deserializer function.
    :return: an instance of ``cls`` if given, a dict otherwise.
    """
    if type(json_obj) == cls:
        return json_obj
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


class JsonSerializable:
    """
    This class offers an alternative to using the ``jsons.load`` and
    ``jsons.dump`` methods. An instance of a class that inherits from
    ``JsonSerializable`` has the ``json`` property, which value is equivalent
    to calling ``jsons.dump`` on that instance. Furthermore, you can call
    ``from_json`` on that class, which is equivalent to calling ``json.load``
    with that class as an argument.
    """
    @classmethod
    def with_dump(cls, **kwargs) -> type:
        """
        Return a class (``type``) that is based on JsonSerializable with the
        ``dump`` method being automatically provided the given ``kwargs``.

        **Example:**

        >>> custom_serializable = JsonSerializable\
                .with_dump(key_transformer=KEY_TRANSFORMER_CAMELCASE)
        >>> class Person(custom_serializable):
        ...     def __init__(self, my_name):
        ...         self.my_name = my_name
        >>> p = Person('John')
        >>> p.json
        {'myName': 'John'}

        :param kwargs: the keyword args that are automatically provided to the
        ``dump`` method.
        :return: a class with customized behavior.
        """
        def _wrapper(inst, **kwargs_):
            return dump(inst, **{**kwargs_, **kwargs})

        type_ = type(JsonSerializable.__name__, (cls,), {})
        type_.dump = _wrapper
        return type_

    @classmethod
    def with_load(cls, **kwargs) -> type:
        """
        Return a class (``type``) that is based on JsonSerializable with the
        ``load`` method being automatically provided the given ``kwargs``.

        **Example:**

        >>> custom_serializable = JsonSerializable\
                .with_load(key_transformer=KEY_TRANSFORMER_SNAKECASE)
        >>> class Person(custom_serializable):
        ...     def __init__(self, my_name):
        ...         self.my_name = my_name
        >>> p_json = {'myName': 'John'}
        >>> p = Person.from_json(p_json)
        >>> p.my_name
        'John'

        :param kwargs: the keyword args that are automatically provided to the
        ``load`` method.
        :return: a class with customized behavior.
        """
        @classmethod
        def _wrapper(cls_, inst, **kwargs_):
            return load(inst, cls_, **{**kwargs_, **kwargs})
        type_ = type(JsonSerializable.__name__, (cls,), {})
        type_.load = _wrapper
        return type_

    @property
    def json(self) -> dict:
        """
        See ``jsons.dump``.
        :return: this instance in a JSON representation (dict).
        """
        return self.dump()

    @classmethod
    def from_json(cls: type, json_obj: dict, **kwargs) -> object:
        """
        See ``jsons.load``.
        :param json_obj: a JSON representation of an instance of the inheriting
        class
        :param kwargs: the keyword args are passed on to the deserializer
        function.
        :return: an instance of the inheriting class.
        """
        return cls.load(json_obj, **kwargs)

    def dump(self, **kwargs) -> dict:
        """
        See ``jsons.dump``.
        :param kwargs: the keyword args are passed on to the serializer
        function.
        :return: this instance in a JSON representation (dict).
        """
        return dump(self, **kwargs)

    @classmethod
    def load(cls: type, json_obj: dict, **kwargs) -> object:
        """
        See ``jsons.load``.
        :param kwargs: the keyword args are passed on to the serializer
        function.
        :return: this instance in a JSON representation (dict).
        """
        return load(json_obj, cls, **kwargs)


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
