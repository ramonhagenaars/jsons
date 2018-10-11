"""
This module contains common implementation details of jsons. This module is
private, do not import (from) it directly.
"""
import json
import re
from typing import Dict

VALID_TYPES = (str, int, float, bool, list, tuple, set, dict, type(None))
RFC3339_DATETIME_PATTERN = '%Y-%m-%dT%H:%M:%S'


def dump(obj: object, cls: type = None, fork_inst: type = None,
         **kwargs) -> object:
    """
    Serialize the given ``obj`` to a JSON equivalent type (e.g. dict, list,
    int, ...).

    The way objects are serialized can be finetuned by setting serializer
    functions for the specific type using ``set_serializer``.

    You can also provide ``cls`` to specify that ``obj`` needs to be serialized
    as if it was of type ``cls`` (meaning to only take into account attributes
    from ``cls``). The type ``cls`` must have a ``__slots__`` defined. Any type
    will do, but in most cases you may want ``cls`` to be a base class of
    ``obj``.
    :param obj: a Python instance of any sort.
    :param cls: if given, ``obj`` will be dumped as if it is of type ``type``.
    :param fork_inst: if given, it uses this fork of ``JsonSerializable``.
    :param kwargs: the keyword args are passed on to the serializer function.
    :return: the serialized obj as a JSON type.
    """
    if cls and not hasattr(cls, '__slots__'):
        raise KeyError('Invalid type: "{}", only types that have a __slots__ '
                       'defined are allowed.'.format(cls.__name__))
    cls_ = cls or obj.__class__
    cls_name = cls_.__name__.lower()
    fork_inst = fork_inst or JsonSerializable
    serializer = fork_inst._serializers.get(cls_name, None)
    if not serializer:
        parents = [cls_ser for cls_ser in fork_inst._classes_serializers
                   if isinstance(obj, cls_ser)]
        if parents:
            pname = parents[0].__name__.lower()
            serializer = fork_inst._serializers[pname]
    kwargs_ = {'fork_inst': fork_inst, **kwargs}
    return serializer(obj, cls=cls, **kwargs_)


def load(json_obj: dict, cls: type = None, strict: bool = False,
         fork_inst: type = None, **kwargs) -> object:
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

    If `strict` mode is off and the type of `json_obj` exactly matches `cls`
    then `json_obj` is simply returned.

    :param json_obj: the dict that is to be deserialized.
    :param cls: a matching class of which an instance should be returned.
    :param strict: a bool to determine if a partially deserialized `json_obj`
    is tolerated.
    :param fork_inst: if given, it uses this fork of ``JsonSerializable``.
    :param kwargs: the keyword args are passed on to the deserializer function.
    :return: an instance of ``cls`` if given, a dict otherwise.
    """
    if not strict and type(json_obj) == cls:
        return json_obj
    if type(json_obj) not in VALID_TYPES:
        raise KeyError('Invalid type: "{}", only arguments of the following '
                       'types are allowed: {}'
                       .format(type(json_obj).__name__,
                               ", ".join(typ.__name__ for typ
                                         in VALID_TYPES)))
    cls = cls or type(json_obj)
    deserializer = _get_deserializer(cls, fork_inst)
    kwargs_ = {'strict': strict, 'fork_inst': fork_inst, **kwargs}
    return deserializer(json_obj, cls, **kwargs_)


def _get_deserializer(cls: type, fork_inst: type = None):
    fork_inst = fork_inst or JsonSerializable
    cls_name = cls.__name__ if hasattr(cls, '__name__') \
        else cls.__origin__.__name__
    deserializer = fork_inst._deserializers.get(cls_name.lower(), None)
    if not deserializer:
        parents = [cls_ for cls_ in fork_inst._classes_deserializers
                   if issubclass(cls, cls_)]
        if parents:
            pname = parents[0].__name__.lower()
            deserializer = fork_inst._deserializers[pname]
    return deserializer


class JsonSerializable:
    """
    This class offers an alternative to using the ``jsons.load`` and
    ``jsons.dump`` methods. An instance of a class that inherits from
    ``JsonSerializable`` has the ``json`` property, which value is equivalent
    to calling ``jsons.dump`` on that instance. Furthermore, you can call
    ``from_json`` on that class, which is equivalent to calling ``json.load``
    with that class as an argument.
    """
    _classes_serializers = list()
    _classes_deserializers = list()
    _serializers = dict()
    _deserializers = dict()
    _fork_counter = 0

    @classmethod
    def fork(cls, name: str = None) -> type:
        """
        Create a 'fork' of ``JsonSerializable``: a new ``type`` with a separate
        configuration of serializers and deserializers.
        :param name: the ``__name__`` of the new ``type``.
        :return: a new ``type`` based on ``JsonSerializable``.
        """
        cls._fork_counter += 1
        class_name = name or '{}_fork{}'.format(cls.__name__,
                                                cls._fork_counter)
        result = type(class_name, (cls,), {})
        result._classes_serializers = cls._classes_serializers.copy()
        result._classes_deserializers = cls._classes_deserializers.copy()
        result._serializers = cls._serializers.copy()
        result._deserializers = cls._deserializers.copy()
        result._fork_counter = 0
        return result

    @classmethod
    def with_dump(cls, fork: bool = False, **kwargs) -> type:
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
        :param fork: determines that a new fork is to be created.
        :return: a class with customized behavior.
        """
        def _wrapper(inst, **kwargs_):
            return dump(inst, **{**kwargs_, **kwargs})

        type_ = cls.fork() if fork else cls
        type_.dump = _wrapper
        return type_

    @classmethod
    def with_load(cls, fork: bool = False, **kwargs) -> type:
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
        :param fork: determines that a new fork is to be created.
        :return: a class with customized behavior.
        """
        @classmethod
        def _wrapper(cls_, inst, **kwargs_):
            return load(inst, cls_, **{**kwargs_, **kwargs})
        type_ = cls.fork() if fork else cls
        type_.load = _wrapper
        return type_

    @property
    def json(self) -> object:
        """
        See ``jsons.dump``.
        :return: this instance in a JSON representation (dict).
        """
        return self.dump()

    def __str__(self) -> str:
        """
        See ``jsons.dumps``.
        :return: this instance as a JSON string.
        """
        return self.dumps()

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

    def dump(self, **kwargs) -> object:
        """
        See ``jsons.dump``.
        :param kwargs: the keyword args are passed on to the serializer
        function.
        :return: this instance in a JSON representation (dict).
        """
        return dump(self, fork_inst=self.__class__, **kwargs)

    @classmethod
    def load(cls: type, json_obj: dict, **kwargs) -> object:
        """
        See ``jsons.load``.
        :param kwargs: the keyword args are passed on to the serializer
        function.
        :param json_obj: the object that is loaded into an instance of `cls`.
        :return: this instance in a JSON representation (dict).
        """
        return load(json_obj, cls, fork_inst=cls, **kwargs)

    def dumps(self, **kwargs) -> str:
        """
        See ``jsons.dumps``.
        :param kwargs: the keyword args are passed on to the serializer
        function.
        :return: this instance as a JSON string.
        """
        return dumps(self, fork_inst=self.__class__, **kwargs)

    @classmethod
    def loads(cls: type, json_obj: str, **kwargs) -> object:
        """
        See ``jsons.loads``.
        :param kwargs: the keyword args are passed on to the serializer
        function.
        :param json_obj: the object that is loaded into an instance of `cls`.
        :return: this instance in a JSON representation (dict).
        """
        return loads(json_obj, cls, fork_inst=cls, **kwargs)

    def dumpb(self, **kwargs) -> bytes:
        """
        See ``jsons.dumpb``.
        :param kwargs: the keyword args are passed on to the serializer
        function.
        :return: this instance as a JSON string.
        """
        return dumpb(self, fork_inst=self.__class__, **kwargs)

    @classmethod
    def loadb(cls: type, json_obj: bytes, **kwargs) -> object:
        """
        See ``jsons.loadb``.
        :param kwargs: the keyword args are passed on to the serializer
        function.
        :param json_obj: the object that is loaded into an instance of `cls`.
        :return: this instance in a JSON representation (dict).
        """
        return loadb(json_obj, cls, fork_inst=cls, **kwargs)

    @classmethod
    def set_serializer(cls: type, func: callable, cls_: type,
                       high_prio: bool = True, fork: bool = False) -> type:
        """
        See ``jsons.set_serializer``.
        :param func: the serializer function.
        :param cls_: the type this serializer can handle.
        :param high_prio: determines the order in which is looked for the
        callable.
        :param fork: determines that a new fork is to be created.
        :return: the type on which this method is invoked or its fork.
        """
        type_ = cls.fork() if fork else cls
        set_serializer(func, cls_, high_prio, type_)
        return type_

    @classmethod
    def set_deserializer(cls: type, func: callable, cls_: type,
                         high_prio: bool = True, fork: bool = False) -> type:
        """
        See ``jsons.set_deserializer``.
        :param func: the deserializer function.
        :param cls_: the type this serializer can handle.
        :param high_prio: determines the order in which is looked for the
        callable.
        :param fork: determines that a new fork is to be created.
        :return: the type on which this method is invoked or its fork.
        """
        type_ = cls.fork() if fork else cls
        set_deserializer(func, cls_, high_prio, type_)
        return type_


def dumps(obj: object, jdkwargs: Dict[str, object] = None,
          *args, **kwargs) -> str:
    """
    Extend ``json.dumps``, allowing any Python instance to be dumped to a
    string. Any extra (keyword) arguments are passed on to ``json.dumps``.

    :param obj: the object that is to be dumped to a string.
    :param jdkwargs: extra keyword arguments for ``json.dumps`` (not
    ``jsons.dumps``!)
    :param args: extra arguments for ``jsons.dumps``.
    :param kwargs: Keyword arguments that are passed on through the
    serialization process.
    passed on to the serializer function.
    :return: ``obj`` as a ``str``.
    """
    jdkwargs = jdkwargs or {}
    dumped = dump(obj, *args, **kwargs)
    return json.dumps(dumped, **jdkwargs)


def loads(str_: str, cls: type = None, jdkwargs: Dict[str, object] = None,
          *args, **kwargs) -> object:
    """
    Extend ``json.loads``, allowing a string to be loaded into a dict or a
    Python instance of type ``cls``. Any extra (keyword) arguments are passed
    on to ``json.loads``.

    :param str_: the string that is to be loaded.
    :param cls: a matching class of which an instance should be returned.
    :param jdkwargs: extra keyword arguments for ``json.loads`` (not
    ``jsons.loads``!)
    :param args: extra arguments for ``jsons.loads``.
    :param kwargs: extra keyword arguments for ``jsons.loads``.
    :return: a JSON-type object (dict, str, list, etc.) or an instance of type
    ``cls`` if given.
    """
    jdkwargs = jdkwargs or {}
    obj = json.loads(str_, **jdkwargs)
    return load(obj, cls, *args, **kwargs)


def dumpb(obj: object, encoding: str = 'utf-8',
          jdkwargs: Dict[str, object] = None, *args, **kwargs) -> bytes:
    """
    Extend ``json.dumps``, allowing any Python instance to be dumped to bytes.
    Any extra (keyword) arguments are passed on to ``json.dumps``.

    :param obj: the object that is to be dumped to bytes.
    :param encoding: the encoding that is used to transform to bytes.
    :param jdkwargs: extra keyword arguments for ``json.dumps`` (not
    ``jsons.dumps``!)
    :param args: extra arguments for ``jsons.dumps``.
    :param kwargs: Keyword arguments that are passed on through the
    serialization process.
    passed on to the serializer function.
    :return: ``obj`` as ``bytes``.
    """
    jdkwargs = jdkwargs or {}
    dumped_dict = dump(obj, *args, **kwargs)
    dumped_str = json.dumps(dumped_dict, **jdkwargs)
    return dumped_str.encode(encoding=encoding)


def loadb(bytes_: bytes, cls: type = None, encoding: str = 'utf-8',
          jdkwargs: Dict[str, object] = None, *args, **kwargs) -> object:
    """
    Extend ``json.loads``, allowing bytes to be loaded into a dict or a Python
    instance of type ``cls``. Any extra (keyword) arguments are passed on to
    ``json.loads``.

    :param bytes_: the bytes that are to be loaded.
    :param cls: a matching class of which an instance should be returned.
    :param encoding: the encoding that is used to transform from bytes.
    :param jdkwargs: extra keyword arguments for ``json.loads`` (not
    ``jsons.loads``!)
    :param args: extra arguments for ``jsons.loads``.
    :param kwargs: extra keyword arguments for ``jsons.loads``.
    :return: a JSON-type object (dict, str, list, etc.) or an instance of type
    ``cls`` if given.
    """
    jdkwargs = jdkwargs or {}
    str_ = bytes_.decode(encoding=encoding)
    return loads(str_, cls, jdkwargs=jdkwargs, *args, **kwargs)


def set_serializer(func: callable, cls: type, high_prio: bool = True,
                   fork_inst: type = JsonSerializable) -> None:
    """
    Set a serializer function for the given type. You may override the default
    behavior of ``jsons.load`` by setting a custom serializer.

    The ``func`` argument must take one argument (i.e. the object that is to be
    serialized) and also a ``kwargs`` parameter. For example:

    >>> def func(obj, **kwargs):
    ...    return dict()

    You may ask additional arguments between ``cls`` and ``kwargs``.

    :param func: the serializer function.
    :param cls: the type this serializer can handle.
    :param high_prio: determines the order in which is looked for the callable.
    :param fork_inst: if given, it uses this fork of ``JsonSerializable``.
    :return: None.
    """
    if cls:
        index = 0 if high_prio else len(fork_inst._classes_serializers)
        fork_inst._classes_serializers.insert(index, cls)
        fork_inst._serializers[cls.__name__.lower()] = func
    else:
        fork_inst._serializers['nonetype'] = func


def set_deserializer(func: callable, cls: type, high_prio: bool = True,
                     fork_inst: type = JsonSerializable) -> None:
    """
    Set a deserializer function for the given type. You may override the
    default behavior of ``jsons.dump`` by setting a custom deserializer.

    The ``func`` argument must take two arguments (i.e. the dict containing the
    serialized values and the type that the values should be deserialized into)
    and also a ``kwargs`` parameter. For example:

    >>> def func(dict_, cls, **kwargs):
    ...    return cls()

    You may ask additional arguments between ``cls`` and ``kwargs``.

    :param func: the deserializer function.
    :param cls: the type this serializer can handle.
    :param high_prio: determines the order in which is looked for the callable.
    :param fork_inst: if given, it uses this fork of ``JsonSerializable``.
    :return: None.
    """
    if cls:
        index = 0 if high_prio else len(fork_inst._classes_deserializers)
        fork_inst._classes_deserializers.insert(index, cls)
        fork_inst._deserializers[cls.__name__.lower()] = func
    else:
        fork_inst._deserializers['nonetype'] = func


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
