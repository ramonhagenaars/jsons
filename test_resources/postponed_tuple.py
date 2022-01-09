from __future__ import annotations

from typing import NamedTuple


class Tuplicity(NamedTuple):
    a: int
    b: int


class Tuplicitous(NamedTuple):
    a: int
    b: int
    c: Tuplicity
