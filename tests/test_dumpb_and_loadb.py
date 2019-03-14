import json
from unittest import TestCase
import jsons


class TestDumpbAndLoadb(TestCase):
    def test_dumpb(self):
        class A:
            def __init__(self):
                self.name = 'A'

        class B:
            def __init__(self, a: A):
                self.a = a
                self.name = 'B'

        dumped = jsons.dumpb(B(A()), jdkwargs={'sort_keys': True})
        b = json.dumps({'a': {'name': 'A'}, 'name': 'B'},
                       sort_keys=True).encode()
        self.assertEqual(b, dumped)

    def test_loadb(self):
        class A:
            def __init__(self):
                self.name = 'A'

        class B:
            def __init__(self, a: A):
                self.a = a
                self.name = 'B'

        b = json.dumps({'a': {'name': 'A'}, 'name': 'B'}).encode()
        loaded_dict = jsons.loadb(b)

        self.assertDictEqual(loaded_dict, {'a': {'name': 'A'}, 'name': 'B'})

        loaded_obj = jsons.loadb(b, B)
        self.assertEqual('B', loaded_obj.name)
        self.assertEqual('A', loaded_obj.a.name)
