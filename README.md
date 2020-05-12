[![Python versions](https://img.shields.io/pypi/pyversions/jsons.svg)](https://img.shields.io/pypi/pyversions/jsons.svg)
[![Downloads](https://pepy.tech/badge/jsons)](https://pepy.tech/project/jsons)
[![PyPI version](https://badge.fury.io/py/jsons.svg)](https://badge.fury.io/py/jsons)
[![Code Coverage](https://codecov.io/gh/ramonhagenaars/jsons/branch/master/graph/badge.svg)](https://codecov.io/gh/ramonhagenaars/jsons)
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/ramonhagenaars/jsons/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/ramonhagenaars/jsons/?branch=master)


<p align='center'>
  <a href='https://jsons.readthedocs.io/en/latest/'>
    <img width='150' src='https://github.com/ramonhagenaars/jsons/raw/master/resources/jsons-logo.svg?sanitize=true' />
  </a> 
</p>

  - *Python 3.5+*
  - *Minimal effort to use\!*
  - *No magic, just you, Python and jsons\!*
  - *Human readible JSON without pollution\!*
  - *Easily customizable and extendable\!*
  - *Type hints for the win\!*

💗 this lib? Leave a ★ and tell your colleagues!

Example of a model to serialize:

```python
>>> @dataclass
... class Person:
...    name: str
...    birthday: datetime
...
>>> p = Person('Guido van Rossum', birthday_guido)
```

Example of using jsons to serialize:

```python
>>> out = jsons.dump(p)
>>> out
{'birthday': '1956-01-31T12:00:00Z', 'name': 'Guido van Rossum'}
```

Example of using jsons to deserialize:

```python
>>> p2 = jsons.load(out, Person)
>>> p2
Person(name='Guido van Rossum', birthday=datetime.datetime(1956, 1, 31, 12, 0, tzinfo=datetime.timezone.utc))
```

# Installation

    pip install jsons

# Usage

```python
import jsons

some_instance = jsons.load(some_dict, SomeClass)  # Deserialization
some_dict = jsons.dump(some_instance)  # Serialization
```

In some cases, you have instances that contain other instances that need (de)serialization, for instance with lists or dicts. You can use the
`typing` classes for this as is demonstrated below.

```python
from typing import List, Tuple
import jsons

# For more complex deserialization with generic types, use the typing module
list_of_tuples = jsons.load(some_dict, List[Tuple[AClass, AnotherClass]])
```

(For more examples, see the
[FAQ](https://jsons.readthedocs.io/en/latest/faq.html))

# Documentation 

  - [Main documentation](https://jsons.readthedocs.io/en/latest/)
  - [API docs](https://jsons.readthedocs.io/en/latest/api.html)
  - [FAQ](https://jsons.readthedocs.io/en/latest/faq.html)

# Meta

## Recent updates

### 1.2.0

- Bugfix: Fixed bug with postponed typehints (PEP-563).
- Bugfix: Loading an invalid value targeting an optional did not raise.
- Bugfix: Loading a dict did not properly pass key_transformers.

### 1.1.2

- Feature: Added `__version__` which can be imported from `jsons`
- Bugfix: Dumping a tuple with ellipsis failed in strict mode.

### 1.1.1

  - Feature: Added a serializer for ``Union`` types.
  - Change: Exceptions are more clear upon deserialization failure (thanks to haluzpav).
  - Change: You can no longer announce a class with a custom name.
  - Bugfix: Fixed dumping optional attributes.
  - Bugfix: Dataclasses inheriting from ``JsonSerializable`` always dumped their attributes as if in strict mode. 

### 1.1.0

  - Feature: Added ``strict`` parameter to ``dump`` to indicate that dumping a certain ``cls`` will ignore any extra data.
  - Feature: When using ``dump(obj, cls=x)``, ``x`` can now be any class (previously, only a class with ``__slots__``).
  - Feature: Support for dumping ``Decimal`` (thanks to herdigiorgi).
  - Feature: Primitives are now cast if possible when dumping (e.g. ``dump(5, str)``).
  - Feature: Dumping iterables with generic types (e.g. ``dump(obj, List[str])``) will now dump with respect to that types (if ``strict``)
  - Feature: The ``default_dict`` serializer now optionally accepts types: ``Optional[Dict[str, type]]``.
  - Change: Improved performance when dumping using ``strict=True`` (up to 4 times faster!).
  - Bugfix: ``set_validator`` with multiple types did not work.

### 1.0.0

  - Feature: Added a serializer/deserializer for `time`.
  - Feature: Added a serializer/deserializer for `timezone`.
  - Feature: Added a serializer/deserializer for `timedelta`.
  - Feature: Added a serializer/deserializer for `date`.
  - Bugfix: Dumping verbose did not store the types of dicts (`Dict[K,
    V]`).
  - Bugfix: Loading with `List` (no generic type) failed.
  - Bugfix: Loading with `Dict` (no generic type) failed.
  - Bugfix: Loading with `Tuple` (no generic type) failed.
  

## Contributors

Special thanks to the following contributors of code, discussions or
suggestions:

  - [finetuned89](https://github.com/finetuned89)
  - [haluzpav](https://github.com/haluzpav)
  - [jmolinski](https://github.com/jmolinski)
  - [gastlich](https://github.com/gastlich)
  - [cypreess](https://github.com/cypreess)
  - [casparjespersen](https://github.com/casparjespersen)
  - [ahmetkucuk](https://github.com/ahmetkucuk)
  - [robinklaassen](https://github.com/robinklaassen)
  - [jochembroekhoff](https://github.com/jochembroekhoff)
  - [herdigiorgi](https://github.com/herdigiorgi)
