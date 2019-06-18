|PyPI version| |Docs| |Build Status| |Code Coverage| |Scrutinizer Code Quality|
|Downloads| |Maintainability|

::

       _
      (_)
       _ ___  ___  _ __  ___
      | / __|/ _ \| '_ \/ __|
      | \__ | (_) | | | \__ \
      | |___/\___/|_| |_|___/
     _/ | JSON SERIALIZATION
    |__/      MADE EASY!


*~ Any Python objects to/from JSON, easily! ~*


+--------------------------------------------------------+----------------------------------------------------------------------+
| * *Python 3.5+*                                        | **Example of a model to be serialized:**                             |
|                                                        |                                                                      |
| * *Minimal effort to use!*                             | .. code:: python                                                     |
|                                                        |                                                                      |
| * *No magic, just you, Python and jsons!*              |                                                                      |
|                                                        |     @dataclass                                                       |
| * *Human readible JSON without pollution!*             |     class Person:                                                    |
|                                                        |         name: str                                                    |
| * *Easily customizable and extendable!*                |         birthday: datetime                                           |
|                                                        |                                                                      |
| * *Type hints for the win!*                            | **Example of the serialization:**                                    |
|                                                        |                                                                      |
|                                                        |                                                                      |
|                                                        | .. code:: python                                                     |
|                                                        |                                                                      |
|                                                        |                                                                      |
|                                                        |     jsons.dump(Person('Guido van Rossum', birthday_guido))           |
|                                                        |                                                                      |
|                                                        |                                                                      |
|                                                        | **Output after serialization:**                                      |
|                                                        |                                                                      |
|                                                        |                                                                      |
|                                                        | .. code:: python                                                     |
|                                                        |                                                                      |
|                                                        |                                                                      |
|                                                        |     {'birthday': '1956-01-31T12:00:00Z', 'name': 'Guido van Rossum'} |
+--------------------------------------------------------+----------------------------------------------------------------------+

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

(For more examples, see the
`FAQ <https://jsons.readthedocs.io/en/latest/faq.html>`_)

*************
Documentation
*************
* `Main documentation <https://jsons.readthedocs.io/en/latest/>`_
* `API docs <https://jsons.readthedocs.io/en/latest/api.html>`_
* `FAQ <https://jsons.readthedocs.io/en/latest/faq.html>`_


****
Meta
****

Recent updates
==============

0.9.0
+++++
- Feature: Added the ability to validate instances right after loading.
- Feature: Enhanced typing for the loader functions.
- Change: ``None`` can now be loaded, even in strict-mode.

0.8.9
+++++
- *Breaking change*: Values of primitive types are now cast if possible (e.g. in ``jsons.load('42', int)``).
- Bugfix: NamedTuples could falsely raise an error when a justified ``None`` was provided.
- Feature: Support for ``uuid.UUID``.

0.8.8
+++++
- Feature: Added the ability to dump recursive objects.
- Feature: Clearer messaging upon serialization errors.
- Bugfix: Fix for failing to deserialize UUIDs.

0.8.7
+++++
- *Breaking change*: The default serializers and deserializers now use keyword-only arguments.
- Feature: Added ``strip_attr`` argument for omitting specific attributes when serializing objects.
- Feature: The private attributes from ``ABC`` are now excluded from a dump.

0.8.6
+++++
- Feature: Support for typing.NewType.
- Bugfix: Deserializing a ``Dict[K, V]`` failed in ``3.7``.


Contributors
============
Special thanks to the following contributors of code, discussions or suggestions:


- `finetuned89 <https://github.com/finetuned89>`_
- `haluzpav <https://github.com/haluzpav>`_
- `jmolinski <https://github.com/jmolinski>`_
- `gastlich <https://github.com/gastlich>`_
- `cypreess <https://github.com/cypreess>`_
- `casparjespersen <https://github.com/casparjespersen>`_
- `ahmetkucuk <https://github.com/ahmetkucuk>`_

.. |PyPI version| image:: https://badge.fury.io/py/jsons.svg
   :target: https://badge.fury.io/py/jsons

.. |Docs| image:: https://readthedocs.org/projects/jsons/badge/?version=latest
   :target: https://jsons.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

.. |Build Status| image:: https://api.travis-ci.org/ramonhagenaars/jsons.svg?branch=master
   :target: https://travis-ci.org/ramonhagenaars/jsons

.. |Code Coverage| image:: https://codecov.io/gh/ramonhagenaars/jsons/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/ramonhagenaars/jsons

.. |Scrutinizer Code Quality| image:: https://scrutinizer-ci.com/g/ramonhagenaars/jsons/badges/quality-score.png?b=master
   :target: https://scrutinizer-ci.com/g/ramonhagenaars/jsons/?branch=master

.. |Maintainability| image:: https://api.codeclimate.com/v1/badges/17d997068b3387c2f2c3/maintainability
   :target: https://codeclimate.com/github/ramonhagenaars/jsons/maintainability

.. |Downloads| image:: https://img.shields.io/pypi/dm/jsons.svg
   :target: https://pypistats.org/packages/jsons
