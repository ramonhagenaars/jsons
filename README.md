[![PyPI version](https://badge.fury.io/py/jsons.svg)](https://badge.fury.io/py/jsons)
[![Build Status](https://travis-ci.org/ramonhagenaars/geomodels.svg?branch=master)](https://travis-ci.org/ramonhagenaars/jsons)
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/ramonhagenaars/jsons/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/ramonhagenaars/jsons/?branch=master)
[![Maintainability](https://api.codeclimate.com/v1/badges/17d997068b3387c2f2c3/maintainability)](https://codeclimate.com/github/ramonhagenaars/jsons/maintainability)


# jsons
A Python lib (Python3.5+) for serializing Python objects to dicts or strings and for 
deserializing dicts or strings to Python objects.

## Installation

```
pip install jsons
```

## Usage
```
import jsons


some_instance = jsons.load(some_dict, SomeClass)  # Deserialization
some_dict = jsons.dump(some_instance)  # Serialization
```

## API overview
* ``dump(obj: object) -> dict``: serializes an object to a dict.
* ``load(json_obj: dict, cls: type = None) -> object``: deserializes a dict to an object of type ``cls``.
* ``dumps(obj: object, *args, **kwargs) -> str``: serializes an object to a string.
* ``loads(s: str, cls: type = None, *args, **kwargs) -> object`` deserializes a string to an object of type ``cls``.
* ``set_serializer(c: callable, cls: type) -> None``: sets a custom serialization function for type ``cls``.
* ``set_deserializer(c: callable, cls: type) -> None``: sets a custom deserialization function for type ``cls``.

## Example with dataclasses
```
from dataclasses import dataclass
from typing import List
import jsons


# You can use dataclasses (since Python3.7). Regular Python classes (Python3.5+) will work as well as long as type hints
# are present for custom classes.
@dataclass
class Student:
    name: str


@dataclass
class ClassRoom:
    students: List[Student]


c = ClassRoom([Student('John'), Student('Mary'), Student('Greg'), Student('Susan')])
dumped_c = jsons.dump(c)
print(dumped_c)
# Prints:
# {'students': [{'name': 'John'}, {'name': 'Mary'}, {'name': 'Greg'}, {'name': 'Susan'}]}
loaded_c = jsons.load(dumped_c, ClassRoom)
print(loaded_c)
# Prints:
# ClassRoom(students=[Student(name='John'), Student(name='Mary'), Student(name='Greg'), Student(name='Susan')])

```

## Example with regular classes
```
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


c = ClassRoom([Student('John'), Student('Mary'), Student('Greg'), Student('Susan')])
dumped_c = jsons.dump(c)
print(dumped_c)
# Prints:
# {'students': [{'name': 'John'}, {'name': 'Mary'}, {'name': 'Greg'}, {'name': 'Susan'}]}
loaded_c = jsons.load(dumped_c, ClassRoom)
print(loaded_c)
# Prints:
# <__main__.ClassRoom object at 0x0337F9B0>

```
