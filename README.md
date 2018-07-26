[![PyPI version](https://badge.fury.io/py/jsons.svg)](https://badge.fury.io/py/jsons)
[![Build Status](https://travis-ci.org/ramonhagenaars/geomodels.svg?branch=master)](https://travis-ci.org/ramonhagenaars/jsons)
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/ramonhagenaars/jsons/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/ramonhagenaars/jsons/?branch=master)
[![Maintainability](https://api.codeclimate.com/v1/badges/17d997068b3387c2f2c3/maintainability)](https://codeclimate.com/github/ramonhagenaars/jsons/maintainability)


# jsons
A Python lib (Python3.5+) for deeply serializing Python objects to dicts or strings and for 
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
* ``JsonSerializable``: a base class that allows for convenient use of the jsons features.

## Example with dataclasses
```
from dataclasses import dataclass
from typing import List
import jsons


# You can use dataclasses (since Python3.7). Regular Python classes (Python3.5+) will work as well as long as 
# type hints are present for custom classes.
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
## Example with JsonSerializable
```
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
```

## Advanced features

### Overriding the default (de)serialization behavior
You may alter the behavior of the serialization and deserialization processes yourself by defining your own
custom serialization/deserialization functions.

```
jsons.set_serializer(custom_serializer, datetime)  # A custom datetime serializer.
jsons.set_deserializer(custom_deserializer, str)  # A custom string deserializer.
```

### Transforming the JSON keys
You can have the keys transformed by the serialization or deserialization process by providing a transformer 
function that takes a string and returns a string.

```
result = jsons.dump(some_obj, key_transformer=jsons.KEY_TRANSFORMER_CAMELCASE)
# result could be something like: {'thisIsTransformed': 123}

result = jsons.load(some_dict, SomeClass, key_transformer=jsons.KEY_TRANSFORMER_SNAKECASE)
# result could be something like: {'this_is_transformed': 123}
```

The following casing styles are supported:

```
KEY_TRANSFORMER_SNAKECASE   # snake_case
KEY_TRANSFORMER_CAMELCASE   # camelCase
KEY_TRANSFORMER_PASCALCASE  # PascalCase
KEY_TRANSFORMER_LISPCASE    # lisp-case
```

### Customizing JsonSerializable
If you're using jsons to (de)serialize on multiple locations in your code using 
the same ``kwargs`` every time, you might want to use the `JsonSerializable` 
class. You can extract a dynamic class from `JsonSerializable` with the 
serializing and deserializing methods (`dump`, `load`, ...) overridden, to make
them behave as if these methods are called with your ``kwargs``.

```
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
```
