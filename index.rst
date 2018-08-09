|PyPI version| |Build Status| |Scrutinizer Code Quality|
|Maintainability|

jsons
=====

A Python (3.5+) lib for deeply serializing Python objects to dicts or
strings and for deserializing dicts or strings to Python objects using
type hints.

With ``jsons``, you can serialize/deserialize most objects already. You
can also easily extend ``jsons`` yourself by defining a custom
serializer/deserializer for a certain type. Furthermore, any default
serializer/deserializer can be overridden. Some
serializers/deserializers accept extra parameters to allow you to tune
the serialization/deserialization process to your need.

``jsons`` generates human-readable dicts or JSON strings that are not
polluted with metadata.

Why not use ``__dict__`` for serialization?
'''''''''''''''''''''''''''''''''''''''''''

-  The ``__dict__`` attribute only creates a *shallow* dict of an
   instance. Any contained object is not serialized to a dict.
-  The ``__dict__`` does not take ``@property`` methods in account.
-  Not all objects have a ``__dict__`` attribute (e.g. ``datetime`` does
   not).
-  The serialization process of ``__dict__`` cannot easily be tuned.
-  There is no means to deserialize with ``__dict__``.

Installation
------------

::

   pip install jsons

Usage
-----

::

   import jsons


   some_instance = jsons.load(some_dict, SomeClass)  # Deserialization
   some_dict = jsons.dump(some_instance)  # Serialization

API overview
------------

-  ``dump(obj: object) -> dict``: serializes an object to a dict.
-  ``load(json_obj: dict, cls: type = None) -> object``: deserializes a
   dict to an object of type ``cls``.
-  ``dumps(obj: object, *args, **kwargs) -> str``: serializes an object
   to a string.
-  ``loads(s: str, cls: type = None, *args, **kwargs) -> object``
   deserializes a string to an object of type ``cls``.
-  ``set_serializer(c: callable, cls: type) -> None``: sets a custom
   serialization function for type ``cls``.
-  ``set_deserializer(c: callable, cls: type) -> None``: sets a custom
   deserialization function for type ``cls``.
-  ``JsonSerializable``: a base class that allows for convenient use of
   the jsons features.

Example with dataclasses
------------------------

\``\` from dataclasses import dataclass from typing import List import
jsons

You can use dataclasses (since Python3.7). Regular Python classes (Python3.5+) will work as well as long as
===========================================================================================================

type hints are present for custom classes.
==========================================

@dataclass class Student: name: str

@dataclass class ClassRoom: students: List[Student]

c = ClassRoom([Student(‘John’), Student(‘Mary’), Student(‘Greg’),
Student(‘Susan’)]) dumped_c = jsons.dump(c)

.. |PyPI version| image:: https://badge.fury.io/py/jsons.svg
   :target: https://badge.fury.io/py/jsons
.. |Build Status| image:: https://travis-ci.org/ramonhagenaars/geomodels.svg?branch=master
   :target: https://travis-ci.org/ramonhagenaars/jsons
.. |Scrutinizer Code Quality| image:: https://scrutinizer-ci.com/g/ramonhagenaars/jsons/badges/quality-score.png?b=master
   :target: https://scrutinizer-ci.com/g/ramonhagenaars/jsons/?branch=master
.. |Maintainability| image:: https://api.codeclimate.com/v1/badges/17d997068b3387c2f2c3/maintainability
   :target: https://codeclimate.com/github/ramonhagenaars/jsons/maintainability
