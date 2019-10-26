|PyPI version| |Docs| |Build Status| |Code Coverage| |Scrutinizer Code Quality|
|Downloads| |Maintainability|

.. raw:: html

  <p align="center">
    <img width='150' src='https://github.com/ramonhagenaars/jsons/blob/master/resources/jsons-logo.svg' /> 
  </p>
  
|       

* *Python 3.5+*

* *Minimal effort to use!*

* *No magic, just you, Python and jsons!*

* *Human readible JSON without pollution!*

* *Easily customizable and extendable!*

* *Type hints for the win!*

Example of a model to serialize:

.. code:: python

    >>> @dataclass
    ... class Person:
    ...    name: str
    ...    birthday: datetime
    ...
    >>> p = Person('Guido van Rossum', birthday_guido)

Example of using jsons to serialize:

.. code:: python

    >>> out = jsons.dump(p)
    >>> out
    {'birthday': '1956-01-31T12:00:00Z', 'name': 'Guido van Rossum'}

Example of using jsons to deserialize:

.. code:: python

    >>> p2 = jsons.load(out, Person)
    >>> p2
    Person(name='Guido van Rossum', birthday=datetime.datetime(1956, 1, 31, 12, 0, tzinfo=datetime.timezone.utc))


************
Installation
************

.. image:: https://github.com/ramonhagenaars/jsons/blob/master/resources/jsons-logo.svg
  :align: center
  :width: 20




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

1.0.0
+++++
- Feature: Added a serializer/deserializer for ``time``.
- Feature: Added a serializer/deserializer for ``timezone``.
- Feature: Added a serializer/deserializer for ``timedelta``.
- Feature: Added a serializer/deserializer for ``date``.
- Bugfix: Dumping verbose did not store the types of dicts (``Dict[K, V]``).
- Bugfix: Loading with ``List`` (no generic type) failed.
- Bugfix: Loading with ``Dict`` (no generic type) failed.
- Bugfix: Loading with ``Tuple`` (no generic type) failed.

0.10.2
++++++
- Bugfix: Loading ``Dict[K, V]`` did not parse ``K``.

0.10.1
++++++
- Change: Correction of the type hints of ``load``, ``loads``, ``loadb``.

0.10.0
++++++
- Feature: Added a deserializer for complex numbers.

0.9.0
+++++
- Feature: Added the ability to validate instances right after loading.
- Feature: Enhanced typing for the loader functions.
- Feature: Added the ability to use multiple processes or threads with deserializing lists.
- Feature: Added the ``jsons.fork()`` function.
- Change: ``None`` can now be loaded with the right type hints, even in strict-mode.
- Bugfix: A fork from ``JsonSerializable`` did not copy its settings.


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
- `robinklaassen <https://github.com/robinklaassen>`_
- `jochembroekhoff <https://github.com/jochembroekhoff>`_

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
