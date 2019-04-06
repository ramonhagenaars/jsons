from typing import Optional
from unittest import TestCase
import jsons


class C:
    def __init__(self, x: 'str'):
        self.x = x


class Node:
    def __init__(self, value: int, next: Optional['Node'] = None):
        self.value = value
        self.next = next


class TestVarious(TestCase):
    def test_load_obj_with_str_hint(self):
        loaded = jsons.load({'x': 'test'}, C)
        self.assertEqual('test', loaded.x)

    def test_load_obj_with_str_cls(self):
        loaded = jsons.load({'x': 'test'}, 'tests.test_various.C')
        self.assertEqual('test', loaded.x)

    def test_dump_recursive_structure(self):
        linkedlist = Node(10, Node(20, Node(30)))
        dumped = jsons.dump(linkedlist)
        expected = {
            'value': 10,
            'next': {
                'value': 20,
                'next': {
                    'value': 30,
                    'next': None
                }
            }
        }
        self.assertDictEqual(expected, dumped)

    def test_load_recursive_structure(self):
        source = {
            'value': 10,
            'next': {
                'value': 20,
                'next': {
                    'value': 30,
                    'next': None
                }
            }
        }
        loaded = jsons.load(source, Node)
        self.assertEqual(30, loaded.next.next.value)
