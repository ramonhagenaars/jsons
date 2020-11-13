from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict, Optional
from unittest import TestCase

from jsons._compatibility_impl import Flag

import jsons

from test_resources.postposned_dataclass import A

class TestObject(TestCase):
    def test_dump_object(self):
        @dataclass
        class Wrap:
            a: A

            def __init__(self, a : Optional[A] = None):
                self.a = a if a is not None else A()

        obj = Wrap()
        exp = {'a' : {'a': 42} }
        dump = jsons.dump(obj)
        self.assertDictEqual(exp, dump)
        
        undump = jsons.load(dump, cls = Wrap)
        self.assertEqual(undump, obj)

