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

  - *Turn Python objects into dicts or (json)strings and back*
  - *No changes required to your objects*
  - *Easily customizable and extendable*
  - *Works with dataclasses, attrs and POPOs*

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

### 1.6.3

- Bugfix: a string was sometimes unintentionally parsed into a datetime.

### 1.6.2

- Bugfix: `fork_inst`s were not propagated in `default_list_deserializer` (thanks to patrickguenther).

### 1.6.1

- Bugfix: Loading dicts with hashed keys could cause an error due to being loaded twice (thanks to georgeharker).
- Bugfix: IntEnums were not serialized with their names when `use_enum_name=True` (thanks to georgeharker).
- Bugfix: Named tuples did not use `typing.get_type_hints` for getting the types, causing trouble in future annotations (thanks to georgeharker).

### 1.6.0

- Feature: Support for Python3.10.
- Feature: Support for `attrs`.

### 1.5.1

- Bugfix: `ZoneInfo` failed to dump if attached to a `datetime`.

### 1.5.0

- Feature: Support for `ZoneInfo` on Python3.9+.
- Change: microseconds are no longer stripped by default (thanks to pietrodn).

### 1.4.2

- Bugfix: get_origin did not work with python3.9+ parameterized collections (e.g. `dict[str, str]`).

### 1.4.1

- Bugfix: Types of attributes that are not in the constructor were not properly looked for. See issue #128.

### 1.4.0

- Feature: DefaultDicts can now be deserialized.
- Feature: Dicts with any (hashable) key can now be dumped and loaded.
- Feature: Suppress specific warnings.
- Bugfix: Loading a verbose-serialized object in a list could sometimes deserialize that object as a parent class.
- Bugfix: Unwanted stringification of NoneValues is now prevented in Optionals and Unions with NoneType.
- Bugfix: Fixed a bug with postponed annotations and dataclasses. See also [Issue34776](https://bugs.python.org/issue34776).
- Bugfix: Types of attributes that are not in the constructor are now looked for in __annotations__.

### 1.3.1

- Bugfix: Fixed bug where classmethods were included in the serialized result.

### 1.3.0

- Feature: Added `warn_on_fail` parameter to `default_list_deserializer` that allows to continue deserialization upon errors.
- Feature: Added `transform` that can transform an object to an object of another type.
- Feature: Added serializer and deserializer for `pathlib.Path` (thanks to alexmirrington).
- Change: When loading a list fails, the error message now points to the failing index.
- Bugfix: Fixed bug when dumping an object with an innerclass. 

### 1.2.0

- Bugfix: Fixed bug with postponed typehints (PEP-563).
- Bugfix: Loading an invalid value targeting an optional did not raise.
- Bugfix: Loading a dict did not properly pass key_transformers.
- Bugfix: Loading a namedtuple did not properly use key_transformers.
- Bugfix: Utilized `__annotations__` in favor `_field_types` because of deprecation as of 3.8.

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

[patrickguenther](https://github.com/patrickguenther),
[davetapley](https://github.com/davetapley),
[pietrodn](https://github.com/pietrodn),
[georgeharker](https://github.com/georgeharker),
[aecay](https://github.com/aecay),
[bibz](https://github.com/bibz),
[thijss](https://github.com/Thijss),
[alexmirrington](https://github.com/alexmirrington),
[tirkarthi](https://github.com/tirkarthi), 
[marksomething](https://github.com/marksomething), 
[herdigiorgi](https://github.com/herdigiorgi), 
[jochembroekhoff](https://github.com/jochembroekhoff), 
[robinklaassen](https://github.com/robinklaassen), 
[ahmetkucuk](https://github.com/ahmetkucuk), 
[casparjespersen](https://github.com/casparjespersen), 
[cypreess](https://github.com/cypreess), 
[gastlich](https://github.com/gastlich), 
[jmolinski](https://github.com/jmolinski), 
[haluzpav](https://github.com/haluzpav), 
[finetuned89](https://github.com/finetuned89)
