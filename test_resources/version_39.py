from __future__ import annotations

from dataclasses import dataclass


@dataclass
class C:
    d: dict[str, int]
    l: list[int]
