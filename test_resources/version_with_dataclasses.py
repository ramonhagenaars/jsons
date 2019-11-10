import uuid
from dataclasses import dataclass
from typing import NamedTuple, Optional, Union, Any


@dataclass
class Person:
    name: str


@dataclass
class User:
    user_uuid: uuid.UUID
    name: str


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
