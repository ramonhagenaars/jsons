from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from version_with_dataclasses import A


@dataclass
class Wrap:
    a: A

    def __init__(self, a: Optional[A] = None):
        self.a = a if a is not None else A()
