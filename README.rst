|PyPI version| |Docs| |Build Status| |Scrutinizer Code Quality|
|Maintainability|

=====
jsons
=====

*~ Any Python objects to/from JSON, easily! ~*

A Python (3.5+) lib for easily and deeply serializing Python objects to dicts
or strings and for deserializing dicts or strings to Python objects using type
hints.

With ``jsons``, you can serialize/deserialize most objects already. You
can also easily extend ``jsons`` yourself by defining a custom
serializer/deserializer for a certain type. Furthermore, any default
serializer/deserializer can be overridden. Some
serializers/deserializers accept extra parameters to allow you to tune
the serialization/deserialization process to your need.

``jsons`` generates human-readable dicts or JSON strings that are not
polluted with metadata.

*******************************************
Why not use ``__dict__`` for serialization?
*******************************************
-  The ``__dict__`` attribute only creates a *shallow* dict of an
   instance. Any contained object is not serialized to a dict.
-  The ``__dict__`` does not take ``@property`` methods in account.
-  Not all objects have a ``__dict__`` attribute (e.g. ``datetime`` does
   not).
-  The serialization process of ``__dict__`` cannot easily be tuned.
-  There is no means to deserialize with ``__dict__``.

******************************************
Why not use the standard ``json`` library?
******************************************

- It's quite a hassle to (de)serialize custom types: you need to
  write a subclass of ``json.JSONEncoder`` with specific
  serialization/deserialization code per custom class.
- You will need to provide that subclass of ``json.JSONEncoder`` to
  ``json.dumps``/``json.loads`` every single time.

************
Installation
************

::

   pip install jsons

*****
Usage
*****

.. code:: python

   import jsons

   some_instance = jsons.load(some_dict, SomeClass)  # Deserialization
   some_dict = jsons.dump(some_instance)  # Serialization

In some cases, you have instances that contain other instances that need
(de)serialization, for instance with lists or dicts. You can use the
``typing`` classes for this as is demonstrated below.

.. code:: python

   from typing import List, Tuple
   import jsons

   # For more complex deserialization with generic types, use the typing module
   list_of_tuples = jsons.load(some_dict, List[Tuple[AClass, AnotherClass]])

*****************
API DOCUMENTATION
*****************

See the separate documentation page:

`Documentation <https://github.com/ramonhagenaars/jsons/blob/master/API_DOCUMENTATION.rst>`_

********
Examples
********

Example with dataclasses
========================

.. code:: python

   from dataclasses import dataclass
   from typing import List
   import jsons


   # You can use dataclasses (since Python3.7). Regular Python classes
   # (Python3.5+) will work as well as long as type hints are present for
   # custom classes.
   @dataclass
   class Student:
       name: str


   @dataclass
   class ClassRoom:
       students: List[Student]


   c = ClassRoom([Student('John'), Student('Mary'),
                 Student('Greg'), Student('Susan')])
   dumped_c = jsons.dump(c)
   print(dumped_c)
   # Prints:
   # {'students': [{'name': 'John'}, {'name': 'Mary'},
   # {'name': 'Greg'}, {'name': 'Susan'}]}
   loaded_c = jsons.load(dumped_c, ClassRoom)
   print(loaded_c)
   # Prints:
   # ClassRoom(students=[Student(name='John'), Student(name='Mary'),
   #           Student(name='Greg'), Student(name='Susan')])

Example with regular classes
============================

.. code:: python

   from typing import List
   import jsons


   class Student:
       # Since ``name`` is expected to be a string, no type hint is required.
       def __init__(self, name):
           self.name = name


   class ClassRoom:
       # Since ``Student`` is a custom class, a type hint must be given.
       def __init__(self, students: List[Student]):
           self.students = students


   c = ClassRoom([Student('John'), Student('Mary'),
                 Student('Greg'), Student('Susan')])
   dumped_c = jsons.dump(c)
   print(dumped_c)
   # Prints:
   # {'students': [{'name': 'John'}, {'name': 'Mary'},
   # {'name': 'Greg'}, {'name': 'Susan'}]}
   loaded_c = jsons.load(dumped_c, ClassRoom)
   print(loaded_c)
   # Prints:
   # <__main__.ClassRoom object at 0x0337F9B0>

Example with JsonSerializable
=============================

.. code:: python

   from jsons import JsonSerializable


   class Car(JsonSerializable):
       def __init__(self, color):
           self.color = color

   c = Car('red')
   cj = c.json  # You can also do 'c.dump(**kwargs)'
   print(cj)
   # Prints:
   # {'color': 'red'}
   c2 = Car.from_json(cj)  # You can also do 'Car.load(cj, **kwargs)'
   print(c2.color)
   # Prints:
   # 'red'

*****************
Advanced features
*****************

Using decorators
================

You can decorate a function or method with ``@loaded()`` or ``@dumped()``,
which will respectively load or dump all parameters and the return value.

.. code:: python

   from datetime import datetime
   from jsons.decorators import loaded


   @loaded()
   def some_func(x: datetime) -> datetime:
       # x is now of type datetime.
       return '2018-10-07T19:05:00+02:00'

   result = some_func('2018-10-07T19:05:00+02:00')
   # result is now of type datetime.

In the above case, the type hint could be omitted for the same result: jsons
will recognize the timestamp from the string automatically. In case of a custom
type, you do need a type hint. The same goes for the return type; it could be
omitted in this case as well.

Similarly, you can decorate a function or method with ``@dumped`` as is done
below.

.. code:: python

   from datetime import datetime
   from jsons.decorators import dumped


   class SomeClass:
       @classmethod
       @dumped()
       def some_meth(cls, x):
           # x is now of type str, cls remains untouched.
           return datetime.now()

   result = SomeClass.some_meth(datetime.now())
   # result is now of type str.

In case of methods, like in the example above, the special ``self`` or ``cls``
parameters are not touched by the decorators ``@loaded()`` or ``@dumped()``.
Additionally, you can provide a type hint for any parameter (except ``self`` or
``cls``) or the return value. Doing so will make jsons attempt to dump into
that particular type, just like with
``jsons.dump(some_obj, cls=ParticularType)``.

Both ``@loaded`` and ``@dumped`` can be given the following arguments:

-  ``parameters`` (default ``True``): if positive, parameters will be taken into
   account.
-  ``returnvalue`` (default ``True``): if positive, the return value will be
   taken into account.
-  ``fork_inst`` (default ``JsonSerializable``): if given, this specific
   fork instance will be used for the loading/dumping operations.
-  ``**kwargs``: any other given keyword arguments are passed on to
   ``jsons.load`` or ``jsons.dump``.

The following arguments can be given only to ``@loaded``:

-  ``loader``: a ``jsons`` load function which must be one of ``jsons.load``,
   ``jsons.loads``, ``jsons.loadb``. The given function will be used to load
   from.

The following arguments can be given only to ``@dumped``:

-  ``dumper``: a ``jsons`` dump function which must be one of ``jsons.dump``,
   ``jsons.dumps``, ``jsons.dumpb``. The given function will be used to dump
   with.

Overriding the default (de)serialization behavior
=================================================

You may alter the behavior of the serialization and deserialization processes
yourself by defining your own custom serialization/deserialization functions.

.. code:: python

   jsons.set_serializer(custom_serializer, datetime)  # A custom datetime serializer.
   jsons.set_deserializer(custom_deserializer, str)  # A custom string deserializer.

A custom serializer must have the following form:

.. code:: python

   def someclass_serializer(obj: SomeClass, **kwargs) -> object:
       # obj is the instance that needs to be serialized.
       # Make sure to return a type with a JSON equivalent, one of:
       # (str, int, float, bool, list, dict, None)
       return obj.__dict__

A custom deserializer must have the following form:

.. code:: python

   def someclass_deserializer(obj: object, cls: type = None, **kwargs) -> SomeClass:
       # obj is the instance that needs to be deserialized.
       # cls is the type that is to be returned. In most cases, this is the
       # type of the object before it was serialized.
       return SomeClass(some_arg=obj['some_arg'])

Note that in both cases, if you choose to call any other (de)serializer within
your own, you should also pass the ``**kwargs`` upon calling.

Transforming the JSON keys
==========================
You can have the keys transformed by the serialization or deserialization
process by providing a transformer function that takes a string and returns a
string.

.. code:: python

   result = jsons.dump(some_obj, key_transformer=jsons.KEY_TRANSFORMER_CAMELCASE)
   # result could be something like: {'thisIsTransformed': 123}

   result = jsons.load(some_dict, SomeClass,
                       key_transformer=jsons.KEY_TRANSFORMER_SNAKECASE)
   # result could be something like: {'this_is_transformed': 123}

The following casing styles are supported:

.. code:: python

   KEY_TRANSFORMER_SNAKECASE   # snake_case
   KEY_TRANSFORMER_CAMELCASE   # camelCase
   KEY_TRANSFORMER_PASCALCASE  # PascalCase
   KEY_TRANSFORMER_LISPCASE    # lisp-case

Customizing JsonSerializable
============================
You can customize the behavior of the ``JsonSerializable`` class or extract a
new class from it. This can be useful if you are using ``jsons`` extensively
throughout your project, especially if you wish to have different
(de)serialization styles in different occasions.

.. code:: python

   forked = JsonSerializable.fork()
   forked.set_serializer(custom_serializer, datetime)  # A custom serializer.

   class Person(forked):
       def __init__(self, dt: datetime):
           self.dt = dt

   p = Person('John')
   p.json  # Will contain a serialized dt using 'custom_serializer'.

   jsons.dump(datetime.now())  # Still uses the default datetime serializer.

In the above example, a custom serializer is set to a fork of
``JsonSerializable``. The regular ``jsons.dump`` does not have this custom
serializer and will therefore behave as it used to.

You can also create a fork of a fork. All serializers and deserializers of the
type that was forked, are copied.

You can also define default ``kwargs`` which are then automatically passed as
arguments to the serializing and deserializing methods (``dump``, ``load``,
...). You can use ``with_dump`` and ``with_load`` to set default ``kwargs`` to
the serialization and deserialization process respectively.

.. code:: python

   custom_serializable = JsonSerializable\
       .with_dump(key_transformer=KEY_TRANSFORMER_CAMELCASE)\
       .with_load(key_transformer=KEY_TRANSFORMER_SNAKECASE)

   class Person(custom_serializable):
       def __init__(self, my_name):
           self.my_name = my_name

   p = Person('John')
   p.json  # {'myName': 'John'}  <-- note the camelCase

   p2 = Person.from_json({'myName': 'Mary'})
   p2.my_name  # 'Mary'  <-- note the snake_case in my_name

You can, of course, also do this with a fork of ``JsonSerializable`` or you
can create a fork in the process by setting ``fork=True`` in ``with_dump`` or
``with_load``.

****
Meta
****

Recent updates
==============

0.7.0
+++++
- Doc: Improved API documentation
- Feature: Support for loading Union or Optional
- Feature: Extended strict-mode
- Feature: Added custom Exceptions
- Feature: Support for attr-getters
- Bugfix: local timezone for datetime serialization improved

0.6.1
+++++
- Feature: Support for loading tuples of variable length


Contributors
============
Special thanks to the following contributors:


- `finetuned89 <https://github.com/finetuned89>`_
- `haluzpav <https://github.com/haluzpav>`_

.. |PyPI version| image:: https://badge.fury.io/py/jsons.svg
   :target: https://badge.fury.io/py/jsons

.. |Docs| image:: https://readthedocs.org/projects/jsons/badge/?version=latest
   :target: https://jsons.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

.. |Build Status| image:: https://api.travis-ci.org/ramonhagenaars/jsons.svg?branch=master
   :target: https://travis-ci.org/ramonhagenaars/jsons
.. |Scrutinizer Code Quality| image:: https://scrutinizer-ci.com/g/ramonhagenaars/jsons/badges/quality-score.png?b=master
   :target: https://scrutinizer-ci.com/g/ramonhagenaars/jsons/?branch=master
.. |Maintainability| image:: https://api.codeclimate.com/v1/badges/17d997068b3387c2f2c3/maintainability
   :target: https://codeclimate.com/github/ramonhagenaars/jsons/maintainability
