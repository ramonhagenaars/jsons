import uuid
from dataclasses import dataclass
from typing import NamedTuple, Optional, Union


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
