
::

       _                     
      (_)                    
       _ ___  ___  _ __  ___ 
      | / __|/ _ \| '_ \/ __|
      | \__ | (_) | | | \__ \
      | |___/\___/|_| |_|___/
     _/ | JSON SERIALIZATION                   
    |__/      MADE EASY!               

      Official Documentation  

###
API
###


**************
Main functions
**************

====
dump
====

This is the main serialization function of ``jsons``. It will look for the best fitting
serializer function that is registered and use that to turn the given object to a JSON
compatible type.

Any parameter of a serializer function, can be set using the keyword arguments of ``dump``.
Here is an overview of the standard options:

+--------------------+--------------------------+--------------------------------------------------------+
| **Parameter**      | **Type**                 | **Description**                                        |
+--------------------+--------------------------+--------------------------------------------------------+
| strip_microseconds | ``bool``                 | Microseconds are not included in serialized datetimes. |
+--------------------+--------------------------+--------------------------------------------------------+
| strip_nulls        | ``bool``                 | The resulting JSON will not contain attributes         |
|                    |                          | with values that are ``null``.                         |
+--------------------+--------------------------+--------------------------------------------------------+
| strip_privates     | ``bool``                 | Private attributes (starting with ``_``)               |
|                    |                          | are omitted.                                           |
+--------------------+--------------------------+--------------------------------------------------------+
| strip_properties   | ``bool``                 | Properties (``@property``) are omitted.                |
+--------------------+--------------------------+--------------------------------------------------------+
| use_enum_name      | ``bool``                 | When ``True``, enums are serialized as their           |
|                    |                          | names. Otherwise their values are used.                |
+--------------------+--------------------------+--------------------------------------------------------+
| key_transformer    | ``Callable[[str], str]`` | Transforms the keys of the resulting dict.             |
|                    |                          | For example, ``jsons.KEY_TRANSFORMER_CAMELCASE``       |
|                    |                          | turns all keys in 'camelCase'.                         |
+--------------------+--------------------------+--------------------------------------------------------+
| verbose            | ``verbose:               | This parameter allows you to specify whether and how   |
|                    | Union[Verbosity, bool]`` | meta data should be outputted. If ``WITH_CLASS_INFO``  |
|                    |                          | or ``WITH_EVERYTHING`` is used, the output contain     |
|                    |                          | typing info. With that info ``jsons.load`` does not    |
|                    |                          | need a ``cls`` argument.                               |
+--------------------+--------------------------+--------------------------------------------------------+


Here is an example:

.. code:: python
    
    >>> @dataclass
    ... class C:
    ...     _foo: int
    ...     bar: int
    >>> c = C(1, 2)
    >>> jsons.dump(c, strip_privates=True)
    {'bar': 2}

For more info, check out the parameters of the `serializers`_.

*Function signature:*

+----------------+-------------------------------------------------------------------------------------------------------------------+
| *Function:*    | ``jsons.dump``                                                                                                    |
+----------------+-------------------------------------------------------------------------------------------------------------------+
| *Description:* | Serialize the given object to a JSON compatible type (e.g. dict, list, string, etc.)                              |
+----------------+-------------------------------+-----------------------------------------------------------------------------------+
| *Arguments:*   | ``obj: object``               | The object that is to be serialized.                                              |
+                +-------------------------------+-----------------------------------------------------------------------------------+
|                | ``cls: Optional[type]``       | If given, ``obj`` will be dumped as if it is of type ``type``.                    |
+                +-------------------------------+-----------------------------------------------------------------------------------+
|                | ``fork_inst: Optional[type]`` | If given, the serializer functions of this fork of ``JsonSerializable`` are used. |
+                +-------------------------------+-----------------------------------------------------------------------------------+
|                | ``kwargs``                    | Keyword arguments will be passed on to the serializer functions.                  |
+----------------+-------------------------------+-----------------------------------------------------------------------------------+
| *Returns:*     | ``object``                    | The serialized ``obj`` as a JSON type.                                            |
+----------------+-------------------------------+-----------------------------------------------------------------------------------+
| *Example:*     | .. code:: python                                                                                                  |
|                |                                                                                                                   |
|                |     >>> some_utcdate = datetime.now(tz=timezone.utc)                                                              |
|                |     >>> jsons.dump(some_utcdate)                                                                                  |
|                |     '2019-02-16T20:33:36Z'                                                                                        |
+----------------+-------------------------------------------------------------------------------------------------------------------+

====
load
====

+----------------+---------------------------------------------------------------------------------------------------------------------------------------------------+
| *Function:*    | ``jsons.load``                                                                                                                                    |
+----------------+---------------------------------------------------------------------------------------------------------------------------------------------------+
| *Description:* | Deserialize the given object to a Python equivalent type or an instance of type ``cls`` (if given).                                               |
+----------------+-------------------------------------------------------------+-------------------------------------------------------------------------------------+
| *Arguments:*   | ``json_obj: object``                                        | The object that is to be deserialized.                                              |
+                +-------------------------------------------------------------+-------------------------------------------------------------------------------------+
|                | ``cls: Optional[type]``                                     | A matching class of which an instance should be returned.                           |
+                +-------------------------------------------------------------+-------------------------------------------------------------------------------------+
|                | ``strict: bool``                                            | Determines strict mode (e.g. fail on partly deserialized objects).                  |
+                +-------------------------------------------------------------+-------------------------------------------------------------------------------------+
|                | ``fork_inst: Optional[type]``                               | If given, the deserializer functions of this fork of ``JsonSerializable`` are used. |
+                +-------------------------------------------------------------+-------------------------------------------------------------------------------------+
|                | ``attr_getters: Optional[Dict[str, Callable[[], object]]]`` | A dict that may hold callables that return values for certain attributes.           |
+                +-------------------------------------------------------------+-------------------------------------------------------------------------------------+
|                | ``kwargs``                                                  | Keyword arguments will be passed on to the deserializer functions.                  |
+----------------+-------------------------------------------------------------+-------------------------------------------------------------------------------------+
| *Returns:*     | ``object``                                                  | An object of a Python equivalent type or of ``cls``.                                |
+----------------+-------------------------------------------------------------+-------------------------------------------------------------------------------------+
| *Example:*     | .. code:: python                                                                                                                                  |
|                |                                                                                                                                                   |
|                |     >>> jsons.load('2019-02-16T20:33:36Z', datetime)                                                                                              |
|                |     datetime.datetime(2019, 2, 16, 20, 33, 36, tzinfo=datetime.timezone.utc)                                                                      |
+----------------+---------------------------------------------------------------------------------------------------------------------------------------------------+

=====
dumps
=====

+----------------+--------------------------------------------------------------------------------------------+
| *Function:*    | ``jsons.dumps``                                                                            |
+----------------+--------------------------------------------------------------------------------------------+
| *Description:* | Serialize the given object to a string.                                                    |
+----------------+------------------+-------------------------------------------------------------------------+
| *Arguments:*   | ``obj: object``  | The object that is to be stringified.                                   |
+                +------------------+-------------------------------------------------------------------------+
|                | ``jdkwargs``     | Extra keyword arguments for ``json.dumps`` (not ``jsons.dumps``!)       |
+                +------------------+-------------------------------------------------------------------------+
|                | ``args``         | Extra arguments for ``jsons.dumps``.                                    |
+                +------------------+-------------------------------------------------------------------------+
|                | ``kwargs``       | Keyword arguments that are passed on through the serialization process. |
+----------------+------------------+-------------------------------------------------------------------------+
| *Returns:*     | ``object``       | An object of a Python equivalent type or of ``cls``.                    |
+----------------+------------------+-------------------------------------------------------------------------+
| *Example:*     | .. code:: python                                                                           |
|                |                                                                                            |
|                |     >>> jsons.dumps([1, 2, 3])                                                             |
|                |     '[1, 2, 3]'                                                                            |
+----------------+--------------------------------------------------------------------------------------------+

=====
loads
=====

+----------------+--------------------------------------------------------------------------------------------------------+
| *Function:*    | ``jsons.loads``                                                                                        |
+----------------+--------------------------------------------------------------------------------------------------------+
| *Description:* | Deserialize a given JSON string to a Python equivalent type or an instance of type ``cls`` (if given). |
+----------------+----------------------------+---------------------------------------------------------------------------+
| *Arguments:*   | ``str_: str``              | The string containing the JSON that is to be deserialized.                |
+                +----------------------------+---------------------------------------------------------------------------+
|                | ``cls: Optional[type]``    | A matching class of which an instance should be returned.                 |
+                +----------------------------+---------------------------------------------------------------------------+
|                | ``jdkwargs``               | Extra keyword arguments for ``json.loads`` (not ``jsons.loads``!).        |
+                +----------------------------+---------------------------------------------------------------------------+
|                | ``args``                   | Extra arguments for ``jsons.load``.                                       |
+                +----------------------------+---------------------------------------------------------------------------+
|                | ``kwargs``                 | Keyword arguments that are passed on through the deserialization process. |
+----------------+----------------------------+---------------------------------------------------------------------------+
| *Returns:*     | ``object``                 | An object of a Python equivalent type or of ``cls``.                      |
+----------------+----------------------------+---------------------------------------------------------------------------+
| *Example:*     | .. code:: python                                                                                       |
|                |                                                                                                        |
|                |     >>> jsons.loads('[1, 2, 3]')                                                                       |
|                |     [1, 2, 3]                                                                                          |
+----------------+--------------------------------------------------------------------------------------------------------+

=====
dumpb
=====

+----------------+---------------------------------------------------------------------------------------------+
| *Function:*    | ``jsons.dumpb``                                                                             |
+----------------+---------------------------------------------------------------------------------------------+
| *Description:* | Serialize the given object to bytes that contain JSON.                                      |
+----------------+-------------------+-------------------------------------------------------------------------+
| *Arguments:*   | ``obj: object``   | The object that is to be serialized.                                    |
+                +-------------------+-------------------------------------------------------------------------+
|                | ``encoding: str`` | The encoding that is used to transform from bytes.                      |
+                +-------------------+-------------------------------------------------------------------------+
|                | ``jdkwargs``      | Extra keyword arguments for ``json.dumps`` (not ``jsons.dumps``!)       |
+                +-------------------+-------------------------------------------------------------------------+
|                | ``args``          | Extra arguments for ``jsons.dumps``.                                    |
+                +-------------------+-------------------------------------------------------------------------+
|                | ``kwargs``        | Keyword arguments that are passed on through the serialization process. |
+----------------+-------------------+-------------------------------------------------------------------------+
| *Returns:*     | ``bytes``         | A serialized ``obj`` in bytes.                                          |
+----------------+-------------------+-------------------------------------------------------------------------+
| *Example:*     | .. code:: python                                                                            |
|                |                                                                                             |
|                |     >>> jsons.dumpb([1, 2, 3])                                                              |
|                |     b'[1, 2, 3]'                                                                            |
+----------------+---------------------------------------------------------------------------------------------+

=====
loadb
=====

+----------------+-----------------------------------------------------------------------------------------------------------------+
| *Function:*    | ``jsons.loadb``                                                                                                 |
+----------------+-----------------------------------------------------------------------------------------------------------------+
| *Description:* | Deserialize the given bytes holding JSON to a Python equivalent type or an instance of type ``cls`` (if given). |
+----------------+--------------------------------+--------------------------------------------------------------------------------+
| *Arguments:*   | ``bytes_: bytes``              | The bytes containing the JSON that is to be deserialized.                      |
+                +--------------------------------+--------------------------------------------------------------------------------+
|                | ``cls: Optional[type]``        | A matching class of which an instance should be returned.                      |
+                +--------------------------------+--------------------------------------------------------------------------------+
|                | ``encoding: str``              | The encoding that is used to transform from bytes.                             |
+                +--------------------------------+--------------------------------------------------------------------------------+
|                | ``jdkwargs``                   | Extra keyword arguments for ``json.loads`` (not ``jsons.loads``!)              |
+                +--------------------------------+--------------------------------------------------------------------------------+
|                | ``args``                       | Extra arguments for ``jsons.loads``.                                           |
+                +--------------------------------+--------------------------------------------------------------------------------+
|                | ``kwargs``                     | Keyword arguments that are passed on through the deserialization process.      |
+----------------+--------------------------------+--------------------------------------------------------------------------------+
| *Returns:*     | ``object``                     | An object of a Python equivalent type or of ``cls``.                           |
+----------------+--------------------------------+--------------------------------------------------------------------------------+
| *Example:*     | .. code:: python                                                                                                |
|                |                                                                                                                 |
|                |     >>> jsons.loadb(b'[1, 2, 3]')                                                                               |
|                |     [1, 2, 3]                                                                                                   |
+----------------+-----------------------------------------------------------------------------------------------------------------+

==============
set_serializer
==============

+----------------+---------------------------------------------------------------------------------------------------------------------+
| *Function:*    | ``jsons.set_serializer``                                                                                            |
+----------------+---------------------------------------------------------------------------------------------------------------------+
| *Description:* | Set a serializer function for the given type. The callable must accept                                              |
|                | at least two arguments: the object to serialize and kwargs. It must                                                 |
|                | return an object that has a JSON equivalent type (e.g. dict, list, string, ...).                                    |
|                |                                                                                                                     |
+----------------+--------------------------------------+------------------------------------------------------------------------------+
| *Arguments:*   | ``func: callable``                   | The serializer function.                                                     |
+                +--------------------------------------+------------------------------------------------------------------------------+
|                | ``cls: Union[type, Sequence[type]]`` | The type or sequence of types that ``func`` can serialize.                   |
+                +--------------------------------------+------------------------------------------------------------------------------+
|                | ``high_prio: bool``                  | If ``True``, then ``func`` will take precedence over any other serializer    |
|                |                                      | function that serializes ``cls``.                                            |
+                +--------------------------------------+------------------------------------------------------------------------------+
|                | ``fork_inst``                        | If given, it registers ``func`` to this fork of ``JsonSerializable``, rather |
|                |                                      | than the global ``jsons``.                                                   |
+----------------+--------------------------------------+------------------------------------------------------------------------------+
| *Returns:*     | ``None``                             |                                                                              |
+----------------+--------------------------------------+------------------------------------------------------------------------------+
| *Example:*     | .. code:: python                                                                                                    |
|                |                                                                                                                     |
|                |     >>> jsons.set_serializer(lambda obj, **_: 123, str)                                                             |
|                |     >>> jsons.dump('any string')                                                                                    |
|                |     123                                                                                                             |
+----------------+---------------------------------------------------------------------------------------------------------------------+

================
set_deserializer
================

+----------------+---------------------------------------------------------------------------------------------------------------------+
| *Function:*    | ``jsons.set_deserializer``                                                                                          |
+----------------+---------------------------------------------------------------------------------------------------------------------+
| *Description:* | Set a deserializer function for the given type. The callable must accept                                            |
|                | at least three arguments: the object to deserialize, the type to deserialize                                        |
|                | to and kwargs. It must return a deserialized object of type cls.                                                    |
|                |                                                                                                                     |
+----------------+--------------------------------------+------------------------------------------------------------------------------+
| *Arguments:*   | ``func: callable``                   | The deserializer function.                                                   |
+                +--------------------------------------+------------------------------------------------------------------------------+
|                | ``cls: Union[type, Sequence[type]]`` | The type or sequence of types that ``func`` can deserialize.                 |
+                +--------------------------------------+------------------------------------------------------------------------------+
|                | ``high_prio: bool``                  | If ``True``, then ``func`` will take precedence over any other deserializer  |
|                |                                      | function that serializes ``cls``.                                            |
+                +--------------------------------------+------------------------------------------------------------------------------+
|                | ``fork_inst``                        | If given, it registers ``func`` to this fork of ``JsonSerializable``, rather |
|                |                                      | than the global ``jsons``.                                                   |
+----------------+--------------------------------------+------------------------------------------------------------------------------+
| *Returns:*     | ``None``                             |                                                                              |
+----------------+--------------------------------------+------------------------------------------------------------------------------+
| *Example:*     | .. code:: python                                                                                                    |
|                |                                                                                                                     |
|                |     >>> jsons.set_deserializer(lambda obj, cls, **_: 123, str)                                                      |
|                |     >>> jsons.load('any string')                                                                                    |
|                |     123                                                                                                             |
+----------------+---------------------------------------------------------------------------------------------------------------------+

=================
suppress_warnings
=================

+----------------+-----------------------------------------------------------------------------------------------------------------+
| *Function:*    | ``jsons.set_deserializer``                                                                                      |
+----------------+-----------------------------------------------------------------------------------------------------------------+
| *Description:* | Suppress (or stop suppressing) warnings.                                                                        |
|                |                                                                                                                 |
+----------------+----------------------------------+------------------------------------------------------------------------------+
| *Arguments:*   | ``do_suppress: Optional[bool]``  | if ``True``, warnings will be suppressed from now on.                        |
+                +----------------------------------+------------------------------------------------------------------------------+
|                | ``cls: type``                    | The type that ``func`` can deserialize.                                      |
+                +----------------------------------+------------------------------------------------------------------------------+
|                | ``high_prio: bool``              | If ``True``, then ``func`` will take precedence over any other deserializer  |
|                |                                  | function that serializes ``cls``.                                            |
+                +----------------------------------+------------------------------------------------------------------------------+
|                | ``fork_inst``                    | If given, it only suppresses (or stops suppressing) warnings of the given    |
|                |                                  | fork.                                                                        |
+----------------+----------------------------------+------------------------------------------------------------------------------+
| *Returns:*     | ``None``                         |                                                                              |
+----------------+----------------------------------+------------------------------------------------------------------------------+
| *Example:*     | .. code:: python                                                                                                |
|                |                                                                                                                 |
|                |     >>> jsons.suppress_warnings()                                                                               |
+----------------+-----------------------------------------------------------------------------------------------------------------+

*******
Classes
*******

================
JsonSerializable
================
This class can be used as a base class for your models.

.. code:: python

    @dataclass
    class Car(JsonSerializable):
        color: str
        owner: str

You can now dump your model using the ``json`` property:

.. code:: python

    car = Car('red', 'Gary')
    dumped = car.json  # == jsons.dump(car)


The JSON data can now also be loaded using your model:

.. code:: python

    loaded = Car.from_json(dumped)  # == jsons.load(dumped, Car)

----
fork
----

+----------------+-------------------------------------------------------------------------------------------+
| *Method:*      | *@classmethod*                                                                            |
|                |                                                                                           |
|                | ``jsons.JsonSerializable.fork``                                                           |
+----------------+-------------------------------------------------------------------------------------------+
| *Description:* | Create a 'fork' of ``JsonSerializable``: a new ``type`` with a separate configuration of  |
|                | serializers and deserializers.                                                            |
+----------------+-----------------------------+-------------------------------------------------------------+
| *Arguments:*   | ``name: Optional[str]``     | The name of the new fork (accessable with ``__name__``).    |
+----------------+-----------------------------+-------------------------------------------------------------+
| *Returns:*     | ``type``                    | A new ``type`` based on ``JsonSerializable``.               |
+----------------+-----------------------------+-------------------------------------------------------------+
| *Example:*     | .. code:: python                                                                          |
|                |                                                                                           |
|                |     >>> fork = jsons.JsonSerializable.fork()                                              |
|                |     >>> jsons.set_deserializer(lambda obj, *_, **__: 'Regular!', str)                     |
|                |     >>> fork.set_deserializer(lambda obj, *_, **__: 'Fork!', str)                         |
|                |     >>> jsons.load('any string')                                                          |
|                |     'Regular!'                                                                            |
|                |     >>> jsons.load('any string', fork_inst=fork)                                          |
|                |     'Fork!'                                                                               |
+----------------+-------------------------------------------------------------------------------------------+

---------
with_dump
---------

+----------------+------------------------------------------------------------------------------------------+
| *Method:*      | *@classmethod*                                                                           |
|                |                                                                                          |
|                | ``jsons.JsonSerializable.with_dump``                                                     |
+----------------+------------------------------------------------------------------------------------------+
| *Description:* | Return a class (``type``) that is based on JsonSerializable with the``dump`` method      |
|                | being automatically provided the given ``kwargs``.                                       |
+----------------+--------------------------+---------------------------------------------------------------+
| *Arguments:*   | ``fork: Optional[bool]`` | Determines whether a new fork is to be created. See also      |
|                |                          | ``JsonSerializable.fork`` and ``JsonSerializable.with_load``. |
+                +--------------------------+---------------------------------------------------------------+
|                | ``kwargs``               | Any keyword arguments that are to be passed on through the    |
|                |                          | serialization process.                                        |
+----------------+--------------------------+---------------------------------------------------------------+
| *Returns:*     | ``type``                 | Returns the ``JsonSerializable`` class or its fork (to allow  |
|                |                          | you to stack).                                                |
+----------------+--------------------------+---------------------------------------------------------------+
| *Example:*     | .. code:: python                                                                         |
|                |                                                                                          |
|                |     >>> @dataclass                                                                       |
|                |     ... class Person(JsonSerializable                                                    |
|                |     ...              .with_dump(key_transformer=KEY_TRANSFORMER_CAMELCASE)               |
|                |     ...              .with_load(key_transformer=KEY_TRANSFORMER_SNAKECASE)):             |
|                |     ...     first_name: str                                                              |
|                |     ...     last_name: str                                                               |
|                |     >>> Person('Johnny', 'Jones').json                                                   |
|                |     {'firstName': 'Johnny', 'lastName': 'Jones'}                                         |
+----------------+------------------------------------------------------------------------------------------+

----
json
----

+----------------+-----------------------------------------------+
| *Method:*      | @property                                     |
|                |                                               |
|                | ``jsons.JsonSerializable.json``               |
+----------------+-----------------------------------------------+
| *Description:* | See ``jsons.dump``.                           |
+----------------+------------------------+----------------------+
| *Arguments:*   | ``kwargs``             | See ``jsons.dump``.  |
+----------------+------------------------+----------------------+
| *Returns:*     | ``object``             | See ``jsons.dump``.  |
+----------------+------------------------+----------------------+
| *Example:*     | .. code:: python                              |
|                |                                               |
|                |     >>> @dataclass                            |
|                |     ... class Person(jsons.JsonSerializable): |
|                |     ...     name: str                         |
|                |     >>> Person('Johnny').json                 |
|                |     {"name": "Johnny"}                        |
+----------------+-----------------------------------------------+

----
dump
----

+----------------+-----------------------------------------------+
| *Method:*      | ``jsons.JsonSerializable.dump``               |
+----------------+-----------------------------------------------+
| *Description:* | See ``jsons.dump``.                           |
+----------------+------------------------+----------------------+
| *Arguments:*   | ``kwargs``             | See ``jsons.dump``.  |
+----------------+------------------------+----------------------+
| *Returns:*     | ``object``             | See ``jsons.dump``.  |
+----------------+------------------------+----------------------+
| *Example:*     | .. code:: python                              |
|                |                                               |
|                |     >>> @dataclass                            |
|                |     ... class Person(jsons.JsonSerializable): |
|                |     ...     name: str                         |
|                |     >>> Person('Johnny').dump()               |
|                |     {"name": "Johnny"}                        |
+----------------+-----------------------------------------------+

-----
dumps
-----

+----------------+------------------------------------------------+
| *Method:*      | ``jsons.JsonSerializable.dumps``               |
+----------------+------------------------------------------------+
| *Description:* | See ``jsons.dumps``.                           |
+----------------+------------------------+-----------------------+
| *Arguments:*   | ``kwargs``             | See ``jsons.dumps``.  |
+----------------+------------------------+-----------------------+
| *Returns:*     | ``object``             | See ``jsons.dumps``.  |
+----------------+------------------------+-----------------------+
| *Example:*     | .. code:: python                               |
|                |                                                |
|                |     >>> @dataclass                             |
|                |     ... class Person(jsons.JsonSerializable):  |
|                |     ...     name: str                          |
|                |     >>> Person('Johnny').dumps()               |
|                |     '{"name": "Johnny"}'                       |
+----------------+------------------------------------------------+

-----
dumpb
-----

+----------------+------------------------------------------------+
| *Method:*      | ``jsons.JsonSerializable.dumpb``               |
+----------------+------------------------------------------------+
| *Description:* | See ``jsons.dumpb``.                           |
+----------------+------------------------+-----------------------+
| *Arguments:*   | ``kwargs``             | See ``jsons.dumpb``.  |
+----------------+------------------------+-----------------------+
| *Returns:*     | ``object``             | See ``jsons.dumpb``.  |
+----------------+------------------------+-----------------------+
| *Example:*     | .. code:: python                               |
|                |                                                |
|                |     >>> @dataclass                             |
|                |     ... class Person(jsons.JsonSerializable):  |
|                |     ...     name: str                          |
|                |     >>> Person('Johnny').dumpb()               |
|                |     b'{"name": "Johnny"}'                      |
+----------------+------------------------------------------------+

---------
from_json
---------

+----------------+-----------------------------------------------+
| *Method:*      | *@classmethod*                                |
|                |                                               |
|                | ``jsons.JsonSerializable.from_json``          |
+----------------+-----------------------------------------------+
| *Description:* | See ``jsons.load``.                           |
+----------------+------------------------+----------------------+
| *Arguments:*   | ``json_obj: object``   | See ``jsons.load``.  |
+                +------------------------+----------------------+
|                | ``kwargs``             | See ``jsons.load``.  |
+----------------+------------------------+----------------------+
| *Returns:*     | ``object``             | See ``jsons.load``.  |
+----------------+------------------------+----------------------+
| *Example:*     | .. code:: python                              |
|                |                                               |
|                |     >>> @dataclass                            |
|                |     ... class Person(jsons.JsonSerializable): |
|                |     ...     name: str                         |
|                |     >>> Person.from_json({'name': 'Johnny'})  |
|                |     '{"name": "Johnny"}'                      |
+----------------+-----------------------------------------------+

----
load
----

+----------------+-----------------------------------------------+
| *Method:*      | *@classmethod*                                |
|                |                                               |
|                | ``jsons.JsonSerializable.load``               |
+----------------+-----------------------------------------------+
| *Description:* | See ``jsons.load``.                           |
+----------------+------------------------+----------------------+
| *Arguments:*   | ``json_obj: object``   | See ``jsons.load``.  |
+                +------------------------+----------------------+
|                | ``kwargs``             | See ``jsons.load``.  |
+----------------+------------------------+----------------------+
| *Returns:*     | ``object``             | See ``jsons.load``.  |
+----------------+------------------------+----------------------+
| *Example:*     | .. code:: python                              |
|                |                                               |
|                |     >>> @dataclass                            |
|                |     ... class Person(jsons.JsonSerializable): |
|                |     ...     name: str                         |
|                |     >>> Person.load({'name': 'Johnny'})       |
|                |     '{"name": "Johnny"}'                      |
+----------------+-----------------------------------------------+

-----
loads
-----

+----------------+------------------------------------------------+
| *Method:*      | *@classmethod*                                 |
|                |                                                |
|                | ``jsons.JsonSerializable.loads``               |
+----------------+------------------------------------------------+
| *Description:* | See ``jsons.loads``.                           |
+----------------+------------------------+-----------------------+
| *Arguments:*   | ``json_obj: object``   | See ``jsons.loads``.  |
+                +------------------------+-----------------------+
|                | ``kwargs``             | See ``jsons.loads``.  |
+----------------+------------------------+-----------------------+
| *Returns:*     | ``object``             | See ``jsons.loads``.  |
+----------------+------------------------+-----------------------+
| *Example:*     | .. code:: python                               |
|                |                                                |
|                |     >>> @dataclass                             |
|                |     ... class Person(jsons.JsonSerializable):  |
|                |     ...     name: str                          |
|                |     >>> Person.loads('{"name": "Johnny"}')     |
|                |     '{"name": "Johnny"}'                       |
+----------------+------------------------------------------------+

-----
loadb
-----

+----------------+------------------------------------------------+
| *Method:*      | *@classmethod*                                 |
|                |                                                |
|                | ``jsons.JsonSerializable.loadb``               |
+----------------+------------------------------------------------+
| *Description:* | See ``jsons.loadb``.                           |
+----------------+------------------------+-----------------------+
| *Arguments:*   | ``json_obj: object``   | See ``jsons.loadb``.  |
+                +------------------------+-----------------------+
|                | ``kwargs``             | See ``jsons.loadb``.  |
+----------------+------------------------+-----------------------+
| *Returns:*     | ``object``             | See ``jsons.loadb``.  |
+----------------+------------------------+-----------------------+
| *Example:*     | .. code:: python                               |
|                |                                                |
|                |     >>> @dataclass                             |
|                |     ... class Person(jsons.JsonSerializable):  |
|                |     ...     name: str                          |
|                |     >>> Person.loads(b'{"name": "Johnny"}')    |
|                |     '{"name": "Johnny"}'                       |
+----------------+------------------------------------------------+

--------------
set_serializer
--------------

+----------------+--------------------------------------------------------------------------------------------------------------+
| *Method:*      | @classmethod                                                                                                 |
|                |                                                                                                              |
|                | ``jsons.JsonSerializable.set_serializer``                                                                    |
+----------------+--------------------------------------------------------------------------------------------------------------+
| *Description:* | See ``jsons.set_serializer``.                                                                                |
+----------------+-------------------------------+------------------------------------------------------------------------------+
| *Arguments:*   | ``func: callable``            | See ``jsons.set_serializer``.                                                |
+                +-------------------------------+------------------------------------------------------------------------------+
|                | ``cls_: type``                | Note the trailing underscore. See ``cls`` of ``jsons.set_serializer``.       |
+                +-------------------------------+------------------------------------------------------------------------------+
|                | ``high_prio: Optional[bool]`` | See ``jsons.set_serializer``.                                                |
+                +-------------------------------+------------------------------------------------------------------------------+
|                | ``fork: Optional[bool]``      | If ``True``, a fork is created and the serializer is added to that fork.     |
+----------------+-------------------------------+------------------------------------------------------------------------------+
| *Returns:*     | ``type``                      | Returns the ``JsonSerializable`` class or its fork (to allow you to stack).  |
+----------------+-------------------------------+------------------------------------------------------------------------------+
| *Example:*     | .. code:: python                                                                                             |
|                |                                                                                                              |
|                |     >>> class BaseModel(JsonSerializable                                                                     |
|                |     ...                 .set_serializer(lambda obj, cls, **_: obj.upper(), str)):                            |
|                |     ...     pass                                                                                             |
|                |     >>> @dataclass                                                                                           |
|                |     ... class Person(BaseModel):                                                                             |
|                |     ...    name: str                                                                                         |
|                |     >>> Person('Arnold').json                                                                                |
|                |     {'name': 'ARNOLD'}                                                                                       |
+----------------+--------------------------------------------------------------------------------------------------------------+

----------------
set_deserializer
----------------

+----------------+----------------------------------------------------------------------------------------------------------------+
| *Method:*      | @classmethod                                                                                                   |
|                |                                                                                                                |
|                | ``jsons.JsonSerializable.set_deserializer``                                                                    |
+----------------+----------------------------------------------------------------------------------------------------------------+
| *Description:* | See ``jsons.set_deserializer``.                                                                                |
+----------------+-------------------------------+--------------------------------------------------------------------------------+
| *Arguments:*   | ``func: callable``            | See ``jsons.set_deserializer``.                                                |
+                +-------------------------------+--------------------------------------------------------------------------------+
|                | ``cls_: type``                | Note the trailing underscore. See ``cls`` of ``jsons.set_deserializer``.       |
+                +-------------------------------+--------------------------------------------------------------------------------+
|                | ``high_prio: Optional[bool]`` | See ``jsons.set_deserializer``.                                                |
+                +-------------------------------+--------------------------------------------------------------------------------+
|                | ``fork: Optional[bool]``      | If ``True``, a fork is created and the serializer is added to that fork.       |
+----------------+-------------------------------+--------------------------------------------------------------------------------+
| *Returns:*     | ``type``                      | Returns the ``JsonSerializable`` class or its fork (to allow you to stack).    |
+----------------+-------------------------------+--------------------------------------------------------------------------------+
| *Example:*     | .. code:: python                                                                                               |
|                |                                                                                                                |
|                |     >>> class BaseModel(JsonSerializable                                                                       |
|                |     ...                 .set_deserializer(lambda obj, cls, **_: obj.upper(), str)):                            |
|                |     ...     pass                                                                                               |
|                |     >>> @dataclass                                                                                             |
|                |     ... class Person(BaseModel):                                                                               |
|                |     ...    name: str                                                                                           |
|                |     >>> Person.from_json({'name': 'Arnold'})                                                                   |
|                |     {'name': 'ARNOLD'}                                                                                         |
+----------------+----------------------------------------------------------------------------------------------------------------+

=========
Verbosity
=========
An enum that defines the level of verbosity of a serialized object. You can
provide an instance of this enum to the ``dump`` function.

Example:

.. code:: python

    @dataclass
    class Car:
        color: str
        owner: str


    c = Car('red', 'me')

Dump it as follows:

.. code:: python

    dumped = jsons.dump(c, verbose=Verbosity.WITH_EVERYTHING)

    # You can also combine Verbosity instances as follows:
    # WITH_CLASS_INFO | WITH_DUMP_TIME

Or the equivalent to ``WITH_EVERYTHING``:

.. code:: python

    dumped = jsons.dump(c, verbose=True)

This would result in the following value for ``dumped``:

.. code:: python

    {
      'color': 'red',
      'owner': 'me',
      '-meta': {
        'classes': {
          '/': '__main__.Car'
        },
        'dump_time': '2019-03-15T19:59:37Z'
      }
    }

And with this, you can deserialize ``dumped`` without having to specify its
class:

.. code:: python

    jsons.load(dumped)

    # Instead of: jsons.load(dumped, cls=Car)

The following are members of ``Verbosity``:

+-----------------+-----------+----------------------------------------------+
| **Attribute**   | **value** | **Description**                              |
+-----------------+-----------+----------------------------------------------+
| WITH_NOTHING    | ``0``     | No meta data is outputted at all.            |
+-----------------+-----------+----------------------------------------------+
| WITH_CLASS_INFO | ``10``    | Just the types of the classes are outputted. |
+-----------------+-----------+----------------------------------------------+
| WITH_DUMP_TIME  | ``20``    | The date/time of dumping is outputted        |
+-----------------+-----------+----------------------------------------------+
| WITH_EVERYTHING | ``30``    | All meta data is outputted.                  |
+-----------------+-----------+----------------------------------------------+

----------
from_value
----------

+----------------+---------------------------------------------------------------------------+
| *Method:*      | *@staticmethod*                                                           |
|                |                                                                           |
|                | ``Verbosity.from_value``                                                  |
+----------------+---------------------------------------------------------------------------+
| *Description:* | Get a ``Verbosity`` instance from a value.                                |
+----------------+----------------+----------------------------------------------------------+
| *Arguments:*   | ``value: any`` | The name of the new fork (accessable with ``__name__``). |
+----------------+----------------+----------------------------------------------------------+
| *Returns:*     | ``Verbosity``  | A new ``type`` based on ``JsonSerializable``.            |
+----------------+----------------+----------------------------------------------------------+
| *Example:*     | .. code:: python                                                          |
|                |                                                                           |
|                |     >>> Verbosity.from_value(True)                                        |
|                |     Verbosity.WITH_EVERYTHING                                             |
|                |                                                                           |
|                |     >>> Verbosity.from_value(None)                                        |
|                |     Verbosity.WITH_NOTHING                                                |
+----------------+---------------------------------------------------------------------------+

**********
Decorators
**********

======
loaded
======

+----------------+---------------------------------------------------------------------------------------------------------------+
| *Decorator:*   | ``jsons.decorators.loaded``                                                                                   |
+----------------+---------------------------------------------------------------------------------------------------------------+
| *Description:* | Call ``jsons.load`` on all parameters and on the return value of the                                          |
|                | decorated function/method.                                                                                    |
|                |                                                                                                               |
+----------------+---------------------------------+-----------------------------------------------------------------------------+
| *Arguments:*   | ``parameters: bool``            | When ``True``, parameters will be 'loaded'.                                 |
+                +---------------------------------+-----------------------------------------------------------------------------+
|                | ``returnvalue: bool``           | When ``True``, the return value is 'loaded' before it is actually returned. |
+                +---------------------------------+-----------------------------------------------------------------------------+
|                | ``fork_inst: JsonSerializable`` | If given, this fork of ``JsonSerializable`` is used to call                 |
|                |                                 | ``load`` on.                                                                |
+                +---------------------------------+-----------------------------------------------------------------------------+
|                | ``loader: callable``            | The load function which must be one of (``load``, ``loads``, ``loadb``).    |
|                +---------------------------------+-----------------------------------------------------------------------------+
|                | ``kwargs``                      | any keyword arguments that should be passed on to ``jsons.load``            |
+----------------+---------------------------------+-----------------------------------------------------------------------------+
| *Example:*     | .. code:: python                                                                                              |
|                |                                                                                                               |
|                |     >>> @loaded()                                                                                             |
|                |     ... def func(arg: datetime) -> datetime:                                                                  |
|                |     ...     # arg is now of type datetime.                                                                    |
|                |     ...     return '2018-10-04T21:57:00Z'                                                                     |
|                |     >>> res = func('2018-10-04T21:57:00Z')                                                                    |
|                |     >>> type(res).__name__                                                                                    |
|                |     'datetime'                                                                                                |
+----------------+---------------------------------------------------------------------------------------------------------------+

======
dumped
======

+----------------+-----------------------------------------------------------------------------------------------------------------+
| *Decorator:*   | ``jsons.decorators.dumped``                                                                                     |
+----------------+-----------------------------------------------------------------------------------------------------------------+
| *Description:* | Call ``jsons.dump`` on all parameters and on the return value of the                                            |
|                | decorated function/method.                                                                                      |
|                |                                                                                                                 |
+----------------+----------------------------------+------------------------------------------------------------------------------+
| *Arguments:*   | ``parameters: bool``             | When ``True``, parameters will be 'dumped'.                                  |
+                +----------------------------------+------------------------------------------------------------------------------+
|                | ``returnvalue: bool``            | When ``True``, the return value is 'dumped' before it is actually returned.  |
+                +----------------------------------+------------------------------------------------------------------------------+
|                | ``fork_inst: JsonSerializable``  | If given, this fork of ``JsonSerializable`` is used to call                  |
|                |                                  | ``dump`` on.                                                                 |
+                +----------------------------------+------------------------------------------------------------------------------+
|                | ``dumper: callable``             | The dump function which must be one of (``dump``, ``dumps`` , ``dumpb``).    |
+                +----------------------------------+------------------------------------------------------------------------------+
|                | ``kwargs``                       | any keyword arguments that should be passed on to ``jsons.dump``             |
+----------------+----------------------------------+------------------------------------------------------------------------------+
| *Example:*     | .. code:: python                                                                                                |
|                |                                                                                                                 |
|                |     >>> @dumped()                                                                                               |
|                |     ... def func(arg):                                                                                          |
|                |     ...     # arg is now of type str                                                                            |
|                |     ...     return datetime.now()                                                                               |
|                |     >>> res = func(datetime.now())                                                                              |
|                |     >>> type(res).__name__                                                                                      |
|                |     'str'                                                                                                       |
+----------------+-----------------------------------------------------------------------------------------------------------------+

***********
Serializers
***********

===========================
default_datetime_serializer
===========================

+----------------+-----------------------------------------------------------------------------------------------+
| *Function:*    | ``jsons.default_datetime_serializer``                                                         |
+----------------+-----------------------------------------------------------------------------------------------+
| *Description:* | Serialize the given datetime instance to a string. It uses                                    |
|                | the RFC3339 pattern. If the datetime is a local time, an                                      |
|                | offset is provided. If datetime is in UTC, the result is                                      |
|                | suffixed with a 'Z'.                                                                          |
+----------------+----------------------------------------+------------------------------------------------------+
| *Arguments:*   | ``obj: datetime``                      | The datetime instance that is to be                  |
|                |                                        | serialized.                                          |
+                +----------------------------------------+------------------------------------------------------+
|                | ``strip_microseconds: Optional[bool]`` | Determines whether microseconds should be discarded. |
+                +----------------------------------------+------------------------------------------------------+
|                | ``kwargs``                             | Not used.                                            |
+----------------+----------------------------------------+------------------------------------------------------+
| *Returns:*     | ``datetime``                           | ``datetime`` as an RFC3339 string.                   |
+----------------+----------------------------------------+------------------------------------------------------+
| *Example:*     | .. code:: python                                                                              |
|                |                                                                                               |
|                |     >>> dt = datetime.now(tz=timezone.utc)                                                    |
|                |     >>> default_datetime_serializer(dt)                                                       |
|                |     '2019-02-28T20:37:42Z'                                                                    |
+----------------+-----------------------------------------------------------------------------------------------+

===========================
default_iterable_serializer
===========================

+----------------+----------------------------------------------------------------------------------------------+
| *Function:*    | ``jsons.default_iterable_serializer``                                                        |
+----------------+----------------------------------------------------------------------------------------------+
| *Description:* | Serialize the given ``obj`` to a list of serialized objects.                                 |
|                |                                                                                              |
+----------------+------------------+---------------------------------------------------------------------------+
| *Arguments:*   | ``obj: object``  | The iterable that is to be serialized.                                    |
+                +------------------+---------------------------------------------------------------------------+
|                | ``kwargs``       | Any keyword arguments that are passed through the serialization process.  |
+----------------+------------------+---------------------------------------------------------------------------+
| *Returns:*     | ``list``         | A list of which all elements are serialized.                              |
+----------------+------------------+---------------------------------------------------------------------------+
| *Example:*     | .. code:: python                                                                             |
|                |                                                                                              |
|                |     >>> default_iterable_serializer((1, 2, 3))                                               |
|                |     [1, 2, 3]                                                                                |
+----------------+------------------------------------------------+---------------------------------------------+

=======================
default_list_serializer
=======================

+----------------+--------------------------------------------------------------------------------------------+
| *Function:*    | ``jsons.default_list_serializer``                                                          |
+----------------+--------------------------------------------------------------------------------------------+
| *Description:* | Serialize the given ``obj`` to a list of serialized objects.                               |
|                |                                                                                            |
+----------------+----------------+---------------------------------------------------------------------------+
| *Arguments:*   | ``obj: list``  | The list that is to be serialized.                                        |
+                +----------------+---------------------------------------------------------------------------+
|                | ``kwargs``     | Any keyword arguments that are passed through the serialization process.  |
+----------------+----------------+---------------------------------------------------------------------------+
| *Returns:*     | ``list``       | A list of which all elements are serialized.                              |
+----------------+----------------+---------------------------------------------------------------------------+
| *Example:*     | .. code:: python                                                                           |
|                |                                                                                            |
|                |     >>> default_iterable_serializer([1, 2, datetime.now(tz=timezone.utc)])                 |
|                |     [1, 2, '2019-02-19T18:41:47Z']                                                         |
+----------------+--------------------------------------------------------------------------------------------+

========================
default_tuple_serializer
========================

+----------------+--------------------------------------------------------------------------------------------+
| Function:*     | ``jsons.default_tuple_serializer``                                                         |
+----------------+--------------------------------------------------------------------------------------------+
| *Description:* | Serialize the given ``obj`` to a list of serialized objects. If ``obj`` happens to be a    |
|                | namedtuple, then ``default_namedtuple_serializer`` is called.                              |
+----------------+----------------+---------------------------------------------------------------------------+
| *Arguments:*   | ``obj: tuple`` | The tuple that is to be serialized.                                       |
+                +----------------+---------------------------------------------------------------------------+
|                | ``kwargs``     | Any keyword arguments that are passed through the serialization process.  |
+----------------+----------------+---------------------------------------------------------------------------+
| *Returns:*     | ``list``       | A list of which all elements are serialized.                              |
+----------------+----------------+---------------------------------------------------------------------------+
| *Example:*     | .. code:: python                                                                           |
|                |                                                                                            |
|                |     >>> default_tuple_serializer((1, 2, datetime.now(tz=timezone.utc)))                    |
|                |     [1, 2, '2019-02-19T18:41:47Z']                                                         |
+----------------+--------------------------------------------------------------------------------------------+

=============================
default_namedtuple_serializer
=============================

+----------------+--------------------------------------------------------------------------------------------+
| Function:*     | ``jsons.default_namedtuple_serializer``                                                    |
+----------------+--------------------------------------------------------------------------------------------+
| *Description:* | Serialize the given ``obj`` to a dict of serialized objects.                               |
|                |                                                                                            |
+----------------+----------------+---------------------------------------------------------------------------+
| *Arguments:*   | ``obj: tuple`` | The tuple that is to be serialized.                                       |
+                +----------------+---------------------------------------------------------------------------+
|                | ``kwargs``     | Any keyword arguments that are passed through the serialization process.  |
+----------------+----------------+---------------------------------------------------------------------------+
| *Returns:*     | ``dict``       | A dict of which all elements are serialized.                              |
+----------------+----------------+---------------------------------------------------------------------------+
| *Example:*     | .. code:: python                                                                           |
|                |                                                                                            |
|                |     >>> Point = namedtuple('Point', ['x', 'y'])                                            |
|                |     >>> default_namedtuple_serializer(Point(10, 20))                                       |
|                |     {'x': 10, 'y': 20}                                                                     |
+----------------+--------------------------------------------------------------------------------------------+

=======================
default_dict_serializer
=======================

+----------------+-----------------------------------------------------------------------------------------------------------------------+
| *Function:*    | ``jsons.default_dict_serializer``                                                                                     |
+----------------+-----------------------------------------------------------------------------------------------------------------------+
| *Description:* | Serialize the given ``obj`` to a dict of serialized objects.                                                          |
|                |                                                                                                                       |
+----------------+-----------------------------------------------------+-----------------------------------------------------------------+
| *Arguments:*   | ``obj: dict``                                       | The object that is to be serialized.                            |
+                +-----------------------------------------------------+-----------------------------------------------------------------+
|                | ``strip_nulls: bool``                               | When ``True``, the resulting dict won't contain 'null values'.  |
+                +-----------------------------------------------------+-----------------------------------------------------------------+
|                | ``key_transformer: Optional[Callable[[str], str]]`` | A function that will be applied to all keys in the              |
|                |                                                     | resulting dict.                                                 |
+                +-----------------------------------------------------+-----------------------------------------------------------------+
|                | ``kwargs``                                          | Any keyword arguments that are passed through the               |
|                |                                                     | serialization process.                                          |
+----------------+-----------------------------------------------------+-----------------------------------------------------------------+
| *Returns:*     | ``dict``                                            | A dict of which all elements are serialized.                    |
+----------------+-----------------------------------------------------+-----------------------------------------------------------------+
| *Example:*     | .. code:: python                                                                                                      |
|                |                                                                                                                       |
|                |     >>> default_dict_serializer({'x': datetime.now()})                                                                |
|                |     {'x': '2019-02-23T13:46:10.650772+01:00'}                                                                         |
+----------------+-----------------------------------------------------------------------------------------------------------------------+

=======================
default_enum_serializer
=======================

+----------------+-----------------------------------------------------------------------------------------------------------+
| *Function:*    | ``jsons.default_enum_serializer``                                                                         |
+----------------+-----------------------------------------------------------------------------------------------------------+
| *Description:* | Serialize the given ``obj`` to a string. By default, the name of the                                      |
|                | enum element is returned.                                                                                 |
|                |                                                                                                           |
+----------------+-----------------------------------------------------+-----------------------------------------------------+
| *Arguments:*   | ``obj: EnumMeta``                                   | The object that is to be serialized.                |
+                +-----------------------------------------------------+-----------------------------------------------------+
|                | ``use_enum_name: bool``                             | When ``True``, the name of the enum type is used,   |
|                |                                                     | otherwise the value is used.                        |
+                +-----------------------------------------------------+-----------------------------------------------------+
|                | ``key_transformer: Optional[Callable[[str], str]]`` | A function that will be applied to all keys in the  |
|                |                                                     | resulting dict.                                     |
+----------------+-----------------------------------------------------+-----------------------------------------------------+
| *Returns:*     | ``str``                                             | A serialized ``obj`` in string format.              |
+----------------+-----------------------------------------------------+-----------------------------------------------------+
| *Example:*     | .. code:: python                                                                                          |
|                |                                                                                                           |
|                |     >>> class Color(Enum):                                                                                |
|                |     ...     RED = 1                                                                                       |
|                |     ...     BLUE = 2                                                                                      |
|                |     >>> jsons.default_enum_serializer(Color.RED)                                                          |
|                |     'RED'                                                                                                 |
+----------------+-----------------------------------------------------------------------------------------------------------+

============================
default_primitive_serializer
============================

+----------------+---------------------------------------------------------------------------------------+
| *Function:*    | ``jsons.default_primitive_serializer``                                                |
+----------------+---------------------------------------------------------------------------------------+
| *Description:* | Serialize the given primitive. This function is just a placeholder; it simply returns |
|                | its parameter.                                                                        |
|                |                                                                                       |
+----------------+----------------------------------------+----------------------------------------------+
| *Arguments:*   | ``obj: object``                        | The primitive object.                        |
+----------------+----------------------------------------+----------------------------------------------+
| *Returns:*     | ``object``                             | ``obj``.                                     |
+----------------+----------------------------------------+----------------------------------------------+
| *Example:*     | .. code:: python                                                                      |
|                |                                                                                       |
|                |     >>> jsons.default_primitive_serializer(42)                                        |
|                |     42                                                                                |
+----------------+---------------------------------------------------------------------------------------+

=========================
default_object_serializer
=========================

+----------------+--------------------------------------------------------------------------------------------------------+
| *Function:*    | ``jsons.default_object_serializer``                                                                    |
+----------------+--------------------------------------------------------------------------------------------------------+
| *Description:* | Serialize the given ``obj`` to a dict. All values within                                               |
|                | ``obj`` are serialized as well.                                                                        |
+----------------+-----------------------------------------------------+--------------------------------------------------+
| *Arguments:*   | ``obj: object``                                     | The object that is to be serialized.             |
+                +-----------------------------------------------------+--------------------------------------------------+
|                | ``key_transformer: Optional[Callable[[str], str]]`` | A function that will be applied to all keys in   |
|                |                                                     | the resulting dict.                              |
+                +-----------------------------------------------------+--------------------------------------------------+
|                | ``strip_nulls: bool``                               | If ``True`` the resulting dict will not contain  |
|                |                                                     | null values.                                     |
+                +-----------------------------------------------------+--------------------------------------------------+
|                | ``strip_privates: bool``                            | If ``True`` the resulting dict will not          |
|                |                                                     | contain private attributes (i.e. attributes      |
|                |                                                     | that start with an underscore).                  |
+                +-----------------------------------------------------+--------------------------------------------------+
|                | ``strip_properties: bool``                          | If ``True`` the resulting dict will not          |
|                |                                                     | contain values from @properties.                 |
+                +-----------------------------------------------------+--------------------------------------------------+
|                | ``verbose: Union[Verbosity, bool]``                 | When set, the output will contain meta data      |
|                |                                                     | (e.g. data on the types).                        |
+                +-----------------------------------------------------+--------------------------------------------------+
|                | ``kwargs``                                          | Any keyword arguments that may be given to the   |
|                |                                                     | serialization process.                           |
+----------------+-----------------------------------------------------+--------------------------------------------------+
| *Returns:*     | ``object``                                          | ``obj``.                                         |
+----------------+-----------------------------------------------------+--------------------------------------------------+
| *Example:*     | .. code:: python                                                                                       |
|                |                                                                                                        |
|                |     >>> class Person:                                                                                  |
|                |     ...     def __init__(self, name: str, friends: Optional[List['Person']] = None):                   |
|                |     ...         self.name = name                                                                       |
|                |     ...         self.friends = friends                                                                 |
|                |     >>> p = Person('Harry', [Person('John')])                                                          |
|                |     >>> jsons.default_object_serializer(p)                                                             |
|                |     {'friends': [{'friends': None, 'name': 'John'}], 'name': 'Harry'}                                  |
+----------------+--------------------------------------------------------------------------------------------------------+

*************
Deserializers
*************

=============================
default_datetime_deserializer
=============================

+----------------+--------------------------------------------------------------------------+
| *Function:*    | ``jsons.default_datetime_deserializer``                                  |
+----------------+--------------------------------------------------------------------------+
| *Description:* | Deserialize a string with an RFC3339 pattern to a datetime instance.     |
+----------------+-------------------------+------------------------------------------------+
| *Arguments:*   | ``obj: str``            | The object that is to be serialized.           |
+                +-------------------------+------------------------------------------------+
|                | ``cls: type``           | Not used.                                      |
+                +-------------------------+------------------------------------------------+
|                | ``kwargs``              | Not used.                                      |
+----------------+-------------------------+------------------------------------------------+
| *Returns:*     | ``object``              | ``datetime``.                                  |
+----------------+-------------------------+------------------------------------------------+
| *Example:*     | .. code:: python                                                         |
|                |                                                                          |
|                |     >>> jsons.default_datetime_deserializer('2019-02-23T22:28:00Z')      |
|                |     datetime.datetime(2019, 2, 23, 22, 28, tzinfo=datetime.timezone.utc) |
+----------------+--------------------------------------------------------------------------+

=========================
default_list_deserializer
=========================

+----------------+----------------------------------------------------------------------------+
| *Function:*    | ``jsons.default_list_deserializer``                                        |
+----------------+----------------------------------------------------------------------------+
| *Description:* | Deserialize a list by deserializing all items of that list.                |
+----------------+----------------------------+-----------------------------------------------+
| *Arguments:*   | ``obj: list``              | The list that needs deserializing.            |
+                +----------------------------+-----------------------------------------------+
|                | ``cls: type``              | Not used.                                     |
+                +----------------------------+-----------------------------------------------+
|                | ``kwargs``                 | Not used.                                     |
+----------------+----------------------------+-----------------------------------------------+
| *Returns:*     | ``list``                   | A deserialized list instance.                 |
+----------------+----------------------------+-----------------------------------------------+
| *Example:*     | .. code:: python                                                           |
|                |                                                                            |
|                |     >>> jsons.default_list_deserializer(['2019-02-23T22:28:00Z'])          |
|                |     [datetime.datetime(2019, 2, 23, 22, 28, tzinfo=datetime.timezone.utc)] |
+----------------+----------------------------------------------------------------------------+

==========================
default_tuple_deserializer
==========================

+----------------+--------------------------------------------------------------------------------------+
| *Function:*    | ``jsons.default_tuple_deserializer``                                                 |
+----------------+--------------------------------------------------------------------------------------+
| *Description:* | Deserialize a (JSON) list into a tuple by deserializing all items                    |
|                | of that list.                                                                        |
+----------------+-------------------------+------------------------------------------------------------+
| *Arguments:*   | ``obj: list``           | The tuple that needs deserializing                         |
+                +-------------------------+------------------------------------------------------------+
|                | ``cls: type``           | The type, optionally with a generic                        |
|                |                         | (e.g. Tuple[str, int]).                                    |
+                +-------------------------+------------------------------------------------------------+
|                | ``kwargs``              | Any keyword arguments that are passed through the          |
|                |                         | deserialization process.                                   |
+----------------+-------------------------+------------------------------------------------------------+
| *Returns:*     | ``tuple``               | A deserialized tuple instance.                             |
+----------------+-------------------------+------------------------------------------------------------+
| *Example:*     | .. code:: python                                                                     |
|                |                                                                                      |
|                |     >>> jsons.default_tuple_deserializer(('2019-02-23T22:28:00Z',), Tuple[datetime]) |
|                |     (datetime.datetime(2019, 2, 23, 22, 28, tzinfo=datetime.timezone.utc),)          |
+----------------+--------------------------------------------------------------------------------------+

===============================
default_namedtuple_deserializer
===============================

+----------------+--------------------------------------------------------------------------------------------+
| *Function:*    | ``jsons.default_namedtuple_deserializer``                                                  |
+----------------+--------------------------------------------------------------------------------------------+
| *Description:* | Deserialize a (JSON) dict or list into a named tuple by deserializing all items of that    |
|                | list/dict.                                                                                 |
|                |                                                                                            |
|                | This deserializer is called by the ``default_tuple_deserializer`` when it notices that     |
|                | a named tuple (rather than a tuple) is involved.                                           |
+----------------+----------------------------+---------------------------------------------------------------+
| *Arguments:*   | ``obj: Union[list, dict]`` | The tuple that needs deserializing.                           |
+                +----------------------------+---------------------------------------------------------------+
|                | ``cls: type``              | The NamedTuple class.                                         |
+                +----------------------------+---------------------------------------------------------------+
|                | ``kwargs``                 | Any keyword arguments that are passed through the             |
|                |                            | deserialization process.                                      |
+----------------+----------------------------+---------------------------------------------------------------+
| *Returns:*     | ``datetime``               | A deserialized named tuple (i.e. an instance of a class).     |
+----------------+----------------------------+---------------------------------------------------------------+
| *Example:*     | .. code:: python                                                                           |
|                |                                                                                            |
|                |     >>> class NT(NamedTuple):                                                              |
|                |     ...     a: int                                                                         |
|                |     ...     b: str = 'I am default'                                                        |
|                |     >>> jsons.load({'a': 42}, NT)                                                          |
|                |     NT(a=42, b='I am default')                                                             |
+----------------+--------------------------------------------------------------------------------------------+

==========================
default_union_deserializer
==========================

+----------------+---------------------------------------------------------------------------------------------------------------------+
| *Function:*    | ``jsons.default_union_deserializer``                                                                                |
+----------------+---------------------------------------------------------------------------------------------------------------------+
| *Description:* | Deserialize an object to any matching type of the given union. The first                                            |
|                | successful deserialization is returned.                                                                             |
+----------------+----------------------------------------+----------------------------------------------------------------------------+
| *Arguments:*   | ``obj: object``                        | The object that needs deserializing.                                       |
+                +----------------------------------------+----------------------------------------------------------------------------+
|                | ``cls: Union``                         | The Union type with a generic (e.g. Union[str, int]).                      |
+                +----------------------------------------+----------------------------------------------------------------------------+
|                | ``kwargs``                             | Any keyword arguments that are passed through the                          |
|                |                                        | deserialization process.                                                   |
+----------------+----------------------------------------+----------------------------------------------------------------------------+
| *Returns:*     | ``object``                             | An object of the first type of the Union that could                        |
|                |                                        | be deserialized successfully.                                              |
+----------------+----------------------------------------+----------------------------------------------------------------------------+
| *Example:*     | .. code:: python                                                                                                    |
|                |                                                                                                                     |
|                |     >>> jsons.default_union_deserializer('2019-02-23T22:28:00Z', Union[List[datetime], datetime])                   |
|                |     datetime.datetime(2019, 2, 23, 22, 28, tzinfo=datetime.timezone.utc)                                            |
+----------------+---------------------------------------------------------------------------------------------------------------------+

========================
default_set_deserializer
========================

+----------------+-----------------------------------------------------------------------------------------------------------------------------------+
| *Function:*    | ``jsons.default_set_deserializer``                                                                                                |
+----------------+-----------------------------------------------------------------------------------------------------------------------------------+
| *Description:* | Deserialize a (JSON) list into a set by deserializing all items of that list. If the set has a generic type (e.g. Set[datetime])  |
|                | then it is assumed that all elements can be deserialized to that type.                                                            |
+----------------+---------------------------------------+-------------------------------------------------------------------------------------------+
| *Arguments:*   | ``obj: object``                       | The list that needs to be deserialized to a set.                                          |
+                +---------------------------------------+-------------------------------------------------------------------------------------------+
|                | ``cls: type``                         | The type of the set, optionally with a generic type (e.g. Set[str]).                      |
+                +---------------------------------------+-------------------------------------------------------------------------------------------+
|                | ``kwargs``                            | Any keyword arguments that are passed through the                                         |
|                |                                       | deserialization process.                                                                  |
+----------------+---------------------------------------+-------------------------------------------------------------------------------------------+
| *Returns:*     | ``set``                               | A deserialized set instance.                                                              |
+----------------+---------------------------------------+-------------------------------------------------------------------------------------------+
| *Example:*     | .. code:: python                                                                                                                  |
|                |                                                                                                                                   |
|                |     >>> jsons.default_set_deserializer(['2019-02-24T17:43:00Z'], Set[datetime])                                                   |
|                |     {datetime.datetime(2019, 2, 24, 17, 43, tzinfo=datetime.timezone.utc)}                                                        |
+----------------+-----------------------------------------------------------------------------------------------------------------------------------+

=========================
default_dict_deserializer
=========================

+----------------+---------------------------------------------------------------------------------------------+
| *Function:*    | ``jsons.default_dict_deserializer``                                                         |
+----------------+---------------------------------------------------------------------------------------------+
| *Description:* | Deserialize a (JSON) object (a dict) and all its content to a Python                        |
|                | dict.                                                                                       |
+----------------+-----------------------------------+---------------------------------------------------------+
| *Arguments:*   | ``obj: dict``                     | The dict that needs to be deserialized.                 |
+                +-----------------------------------+---------------------------------------------------------+
|                | ``cls: type``                     | The type of the dict, optionally with a generic type    |
|                |                                   | (e.g. Dict[str, datetime]).                             |
+                +-----------------------------------+---------------------------------------------------------+
|                | key_transformer:                  | A function that transforms the keys to a                |
|                | Optional[Callable[[str], str]]    | different style (e.g. PascalCase).                      |
+                +-----------------------------------+---------------------------------------------------------+
|                | ``kwargs``                        | Any keyword arguments that are passed through the       |
|                |                                   | deserialization process.                                |
+----------------+-----------------------------------+---------------------------------------------------------+
| *Returns:*     | ``dict``                          | A deserialized dict instance.                           |
+----------------+-----------------------------------+---------------------------------------------------------+
| *Example:*     | .. code:: python                                                                            |
|                |                                                                                             |
|                |     >>> jsons.default_dict_deserializer({'a': '2019-02-24T17:43:00Z'}, Dict[str, datetime]) |
|                |     {'a': datetime.datetime(2019, 2, 24, 17, 43, tzinfo=datetime.timezone.utc)}             |
+----------------+---------------------------------------------------------------------------------------------+

=========================
default_enum_deserializer
=========================

+----------------+-----------------------------------------------------------------------------------------------------------+
| *Function:*    | ``jsons.default_enum_deserializer``                                                                       |
+----------------+-----------------------------------------------------------------------------------------------------------+
| *Description:* | Deserialize an enum value to an enum instance. The serialized value can be either the name or the key of  |
|                | an enum entry. If ``use_enum_name`` is set to ``True``, then the value *must* be the key of the enum      |
|                | entry. If ``use_enum_name`` is set to ``False``, the value *must* be the value of the enum entry. By      |
|                | default, this deserializer tries both.                                                                    |
+----------------+---------------------+-------------------------------------------------------------------------------------+
| *Arguments:*   | ``obj: str``        | The serialized enum.                                                                |
+                +---------------------+-------------------------------------------------------------------------------------+
|                | ``cls: EnumMeta``   | The enum class.                                                                     |
+                +---------------------+-------------------------------------------------------------------------------------+
|                | use_enum_name: bool | Determines whether the name (``True``) or the value (``False``) of an enum element  |
|                |                     | should be used.                                                                     |
+                +---------------------+-------------------------------------------------------------------------------------+
|                | ``kwargs``          | Not used.                                                                           |
+----------------+---------------------+-------------------------------------------------------------------------------------+
| *Returns:*     | ``dict``            | The corresponding enum element instance.                                            |
+----------------+---------------------+-------------------------------------------------------------------------------------+
| *Example:*     | .. code:: python                                                                                          |
|                |                                                                                                           |
|                |     >>> class Color(Enum):                                                                                |
|                |     ...     RED = 1                                                                                       |
|                |     ...     BLUE = 2                                                                                      |
|                |     >>> jsons.default_enum_deserializer('RED', cls=Color)                                                 |
|                |                                                                                                           |
|                |     Color.RED                                                                                             |
+----------------+-----------------------------------------------------------------------------------------------------------+

===========================
default_string_deserializer
===========================

+----------------+-----------------------------------------------------------------------------------------------+
| *Function:*    | ``jsons.default_string_deserializer``                                                         |
+----------------+-----------------------------------------------------------------------------------------------+
| *Description:* | Deserialize a string. If the given ``obj`` can be parsed to a date, a``datetime``             |
|                | instance is returned.                                                                         |
+----------------+-------------------------+---------------------------------------------------------------------+
| *Arguments:*   | ``obj: str``            | The string that is be deserialized.                                 |
+----------------+-------------------------+---------------------------------------------------------------------+
|                | ``cls: Optional[type]`` | Not used.                                                           |
+----------------+-------------------------+---------------------------------------------------------------------+
|                | ``kwargs``              | Any keyword arguments that may be passed on to other deserializers. |
+----------------+-------------------------+---------------------------------------------------------------------+
| *Returns:*     | ``object``              | The deserialized string.                                            |
+----------------+-------------------------+---------------------------------------------------------------------+
| *Example:*     | .. code:: python                                                                              |
|                |                                                                                               |
|                |     >>> jsons.default_string_deserializer('2019-02-24T21:33:00Z')                             |
|                |     2019-02-24 21:33:00+00:00                                                                 |
+----------------+-----------------------------------------------------------------------------------------------+

==============================
default_primitive_deserializer
==============================

+----------------+-----------------------------------------------------------------------------------------+
| *Function:*    | ``jsons.default_primitive_deserializer``                                                |
+----------------+-----------------------------------------------------------------------------------------+
| *Description:* | Deserialize the given primitive. This function is just a placeholder; it simply returns |
|                | its parameter.                                                                          |
+----------------+----------------------------------------+------------------------------------------------+
| *Arguments:*   | ``obj: object``                        | The primitive object.                          |
+                +----------------------------------------+------------------------------------------------+
|                | ``cls: Optional[type]``                | Not used.                                      |
+                +----------------------------------------+------------------------------------------------+
|                | ``kwargs``                             | Not used.                                      |
+----------------+----------------------------------------+------------------------------------------------+
| *Returns:*     | ``object``                             | ``obj``.                                       |
+----------------+----------------------------------------+------------------------------------------------+
| *Example:*     | .. code:: python                                                                        |
|                |                                                                                         |
|                |     >>> jsons.default_primitive_deserializer(42)                                        |
|                |     42                                                                                  |
+----------------+-----------------------------------------------------------------------------------------+

===========================
default_object_deserializer
===========================

+----------------+---------------------------------------------------------------------------------------------------------+
| *Function:*    | ``jsons.default_object_deserializer``                                                                   |
+----------------+---------------------------------------------------------------------------------------------------------+
| *Description:* | Deserialize ``obj`` into an instance of type ``cls``. If ``obj`` contains keys with a certain case      |
|                | style (e.g. camelCase) that do not match the style of ``cls`` (e.g. snake_case), a key_transformer      |
|                | should be used (e.g.KEY_TRANSFORMER_SNAKECASE).                                                         |
+----------------+----------------------------------+----------------------------------------------------------------------+
| *Arguments:*   | ``obj: dict``                    | The object that is be deserialized.                                  |
+                +----------------------------------+----------------------------------------------------------------------+
|                | ``cls: type``                    | The type to which ``obj`` should be deserialized.                    |
+                +----------------------------------+----------------------------------------------------------------------+
|                | ``key_transformer:               | A function that transforms the keys in order to match the attribute  |
|                | Optional[Callable[[str], str]]`` | names of ``cls``.                                                    |
+                +----------------------------------+----------------------------------------------------------------------+
|                | ``strict: bool``                 | When ``True`` deserializes in strict mode.                           |
+                +----------------------------------+----------------------------------------------------------------------+
|                | ``kwargs``                       | Any keyword arguments that may be passed to the deserializers.       |
+----------------+----------------------------------+----------------------------------------------------------------------+
| *Returns:*     | ``object``                       | An instance of type ``cls``.                                         |
+----------------+----------------------------------+----------------------------------------------------------------------+
| *Example:*     | .. code:: python                                                                                        |
|                |                                                                                                         |
|                |     >>> class Person:                                                                                   |
|                |     ...    def __init__(self, name: str, friends: Optional[List['Person']] = None):                     |
|                |     ...        self.name = name                                                                         |
|                |     ...        self.friends = friends                                                                   |
|                |     >>> json_obj = {'friends': [{'friends': None, 'name': 'John'}], 'name': 'Harry'}                    |
|                |     >>> jsons.default_object_deserializer(json_obj, Person)                                             |
|                |     <__main__.Person object at 0x02F84390>                                                              |
+----------------+---------------------------------------------------------------------------------------------------------+
