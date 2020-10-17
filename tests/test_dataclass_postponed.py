from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict, Optional
from unittest import TestCase

from jsons._compatibility_impl import Flag

import jsons

class TestObject(TestCase):
    def test_dump_object(self):
        @dataclass
        class A:
            a: Optional[int] = 42

        obj = A()
        exp = {'a': 42}
        dump = jsons.dump(obj)
        self.assertDictEqual(exp, dump)

