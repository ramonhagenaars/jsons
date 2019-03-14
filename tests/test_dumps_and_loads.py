import json
from unittest import TestCase
import jsons


class TestDumpsAndLoads(TestCase):
    def test_dumps(self):
        class A:
            def __init__(self):
                self.name = 'A'

        class B:
            def __init__(self, a: A):
                self.a = a
                self.name = 'B'

        sdumped = jsons.dumps(B(A()))
        s = json.dumps({'a': {'name': 'A'}, 'name': 'B'})
        self.assertDictEqual(eval(s), eval(sdumped))

    def test_loads(self):
        class A:
            def __init__(self):
                self.name = 'A'

        class B:
            def __init__(self, a: A):
                self.a = a
                self.name = 'B'

        s = json.dumps({'a': {'name': 'A'}, 'name': 'B'})
        loaded_dict = jsons.loads(s)
        self.assertEqual('B', loaded_dict['name'])
        self.assertEqual('A', loaded_dict['a']['name'])

        loaded_obj = jsons.loads(s, B)
        self.assertEqual('B', loaded_obj.name)
        self.assertEqual('A', loaded_obj.a.name)
