from typing import Optional, Type

from jsons._common_impl import StateHolder, T
from jsons._dump_impl import dump, dumps, dumpb
from jsons._fork_impl import fork
from jsons._lizers_impl import set_serializer, set_deserializer
from jsons._load_impl import load, loads, loadb


class JsonSerializable(StateHolder):
    """
    This class offers an alternative to using the ``jsons.load`` and
    ``jsons.dump`` methods. An instance of a class that inherits from
    ``JsonSerializable`` has the ``json`` property, which value is equivalent
    to calling ``jsons.dump`` on that instance. Furthermore, you can call
    ``from_json`` on that class, which is equivalent to calling ``json.load``
    with that class as an argument.
    """

    @classmethod
    def fork(cls, name: Optional[str] = None) -> Type['JsonSerializable']:
        """
        Create a 'fork' of ``JsonSerializable``: a new ``type`` with a separate
        configuration of serializers and deserializers.
        :param name: the ``__name__`` of the new ``type``.
        :return: a new ``type`` based on ``JsonSerializable``.
        """
        return fork(cls, name=name)

    @classmethod
    def with_dump(cls, fork: Optional[bool] = False, **kwargs) \
            -> Type['JsonSerializable']:
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
    def with_load(cls, fork: Optional[bool] = False, **kwargs) \
            -> Type['JsonSerializable']:
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
            return load(inst, cls_, fork_inst=cls_, **{**kwargs_, **kwargs})

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
    def from_json(cls: Type[T], json_obj: object, **kwargs) -> T:
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
    def load(cls: Type[T], json_obj: object, **kwargs) -> T:
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
    def loads(cls: Type[T], json_obj: str, **kwargs) -> T:
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
    def loadb(cls: Type[T], json_obj: bytes, **kwargs) -> T:
        """
        See ``jsons.loadb``.
        :param kwargs: the keyword args are passed on to the serializer
        function.
        :param json_obj: the object that is loaded into an instance of `cls`.
        :return: this instance in a JSON representation (dict).
        """
        return loadb(json_obj, cls, fork_inst=cls, **kwargs)

    @classmethod
    def set_serializer(cls: Type[T],
                       func: callable,
                       cls_: type,
                       high_prio: Optional[bool] = True,
                       fork: Optional[bool] = False) -> T:
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
    def set_deserializer(cls: Type[T],
                         func: callable,
                         cls_: type,
                         high_prio: Optional[bool] = True,
                         fork: Optional[bool] = False) -> T:
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
