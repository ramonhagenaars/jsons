import uuid
from typing import Optional, NewType, Any
from unittest import TestCase

import jsons
from tests.test_specific_versions import only_version_3


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

    def test_dump_load_endless_recursion(self):
        class Narcissus:
            @property
            def mirror(self):
                return self

        n = Narcissus()
        dumped_n = jsons.dump(n)
        loaded_n = jsons.load(dumped_n, Narcissus)
        self.assertTrue(isinstance(loaded_n.mirror.mirror.mirror, Narcissus))

    def test_dump_load_newtype(self):
        Uid = NewType('uid', str)

        class User:
            def __init__(self, uid: Uid, name: str):
                self.uid = uid
                self.name = name

        dumped = jsons.dump(User('uid', 'name'))
        loaded = jsons.load(dumped, User)

        self.assertEqual('uid', loaded.uid)
        self.assertEqual('name', loaded.name)

    def test_any(self):
        class C:
            def __init__(self, a: Any):
                self.a = a

        loaded = jsons.load({'a': 123}, C)
        self.assertEqual(123, loaded.a)

    def test_nonetype(self):
        class C:
            def __init__(self, a: type(None)):
                self.a = a

        loaded = jsons.load({'a': None}, C)
        self.assertEqual(None, loaded.a)
