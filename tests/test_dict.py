import datetime
from enum import Enum
from typing import Dict
from unittest import TestCase
import jsons
from jsons import DeserializationError


class TestDict(TestCase):
    def test_load_dict(self):
        dumped = {'a': {'b': {'c': {'d': '2018-07-08T21:34:00Z'}}}}
        loaded = jsons.load(dumped)
        self.assertEqual(loaded['a']['b']['c']['d'].year, 2018)
        self.assertEqual(loaded['a']['b']['c']['d'].month, 7)
        self.assertEqual(loaded['a']['b']['c']['d'].day, 8)
        self.assertEqual(loaded['a']['b']['c']['d'].hour, 21)
        self.assertEqual(loaded['a']['b']['c']['d'].minute, 34)
        self.assertEqual(loaded['a']['b']['c']['d'].second, 0)

    def test_load_dict_typing(self):
        dumped = {'a': {'b': {'c': {'d': '2018-07-08T21:34:00Z'}}}}
        loaded = jsons.load(dumped, Dict)
        self.assertEqual(loaded['a']['b']['c']['d'].year, 2018)
        self.assertEqual(loaded['a']['b']['c']['d'].month, 7)
        self.assertEqual(loaded['a']['b']['c']['d'].day, 8)
        self.assertEqual(loaded['a']['b']['c']['d'].hour, 21)
        self.assertEqual(loaded['a']['b']['c']['d'].minute, 34)
        self.assertEqual(loaded['a']['b']['c']['d'].second, 0)

    def test_load_dict_with_enum_keys(self):

        class Color(Enum):
            RED = 1
            GREEN = 2
            BLUE = 3

        source1 = {'RED': 255, 'GREEN': 128, 'BLUE': 128}
        source2 = {'red': 255, 'GReeN': 128, 'BlUe': 128}
        expected = {Color.RED: 255, Color.GREEN: 128, Color.BLUE: 128}

        loaded1 = jsons.load(source1, Dict[Color, int])
        self.assertDictEqual(expected, loaded1)

        loaded2 = jsons.load(source2, Dict[Color, int], key_transformer=lambda x: x.upper())
        self.assertDictEqual(expected, loaded2)

    def test_load_dict_with_key_transformers(self):

        class A_:
            def __init__(self, b_: int):
                self.b_ = b_

        class C:
            def __init__(self, a_: A_):
                self.a_ = a_

        src = {
            'a': {
                'b': 42
            }
        }
        loaded = jsons.load(src, key_transformer=lambda x: x + '_')

        expected = {
            'a_': {
                'b_': 42
            }
        }

        self.assertDictEqual(expected, loaded)

    def test_load_dict_with_generic(self):
        class A:
            def __init__(self):
                self.name = 'A'

        class B:
            def __init__(self, a: A):
                self.a = a
                self.name = 'B'

        dumped_b = {'a': {'name': 'A'}, 'name': 'B'}
        dumped_dict = {'b_inst': dumped_b}
        loaded = jsons.load(dumped_dict, Dict[str, B])

        self.assertEqual(loaded['b_inst'].a.name, 'A')

    def test_load_partially_deserialized_dict(self):
        class C:
            def __init__(self, d: datetime.datetime):
                self.d = d

        dat = datetime.datetime(year=2018, month=7, day=8, hour=21, minute=34,
                                tzinfo=datetime.timezone.utc)
        dumped = {'d': dat}
        loaded = jsons.load(dumped, C)

        self.assertEqual(loaded.d, dat)

    def test_load_partially_deserialized_dict_in_strict_mode(self):
        class C:
            def __init__(self, d: datetime.datetime):
                self.d = d

        dat = datetime.datetime(year=2018, month=7, day=8, hour=21, minute=34,
                                tzinfo=datetime.timezone.utc)
        dumped = {'d': dat}
        with self.assertRaises(DeserializationError):
            jsons.load(dumped, C, strict=True)

    def test_dump_dict(self):
        d = datetime.datetime(year=2018, month=7, day=8, hour=21, minute=34,
                              tzinfo=datetime.timezone.utc)
        dict_ = {'a': {'b': {'c': {'d': d}}}}
        expectation = {'a': {'b': {'c': {'d': '2018-07-08T21:34:00Z'}}}}
        self.assertDictEqual(expectation, jsons.dump(dict_))
