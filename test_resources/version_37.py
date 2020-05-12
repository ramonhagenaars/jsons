from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class A:
    x: int


@dataclass
class B:
    a: A
    x: List[int]
