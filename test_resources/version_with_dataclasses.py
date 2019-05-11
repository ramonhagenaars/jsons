import uuid
from dataclasses import dataclass


@dataclass
class Person:
    name: str


@dataclass
class User:
    user_uuid: uuid.UUID
    name: str
