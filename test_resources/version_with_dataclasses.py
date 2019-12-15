import uuid
from dataclasses import dataclass
from typing import NamedTuple, Optional, Union, Any

from jsons import JsonSerializable


@dataclass
class Person:
    name: str


@dataclass
class User:
    user_uuid: uuid.UUID
    name: str


@dataclass
class DataclassWithOptional:
    x: Optional[int]


@dataclass
class HolderWithJsonSerializable(JsonSerializable):
    x: JsonSerializable


class NamedTupleWithOptional(NamedTuple):
    arg: Optional[str]


class NamedTupleWithUnion(NamedTuple):
    arg: Union[str, int, None]


class NamedTupleWithAny(NamedTuple):
    arg: Any


@dataclass
class Parent:
    a: int


@dataclass
class Child(Parent):
    b: int
