from unittest import TestCase

import jsons
from jsons import UnfulfilledArgumentError, DecodeError, DeserializationError


class TestException(TestCase):
    def test_exception_unfulfilled_arg(self):
        class C:
            def __init__(self, x: int, y: int):
                self.x = x
                self.y = y

        with self.assertRaises(UnfulfilledArgumentError):
            jsons.load({"x": 1}, C)

        try:
            jsons.load({"x": 1}, C)
        except UnfulfilledArgumentError as err:
            self.assertDictEqual({"x": 1}, err.source)
            self.assertEqual(C, err.target)
            self.assertEqual('y', err.argument)

    def test_exception_wrong_json(self):
        with self.assertRaises(DecodeError):
            jsons.loads('{this aint no JSON!')

        try:
            jsons.loads('{this aint no JSON!')
        except DecodeError as err:
            self.assertEqual(None, err.target)
            self.assertEqual('{this aint no JSON!', err.source)

    def test_exception_wrong_bytes(self):
        with self.assertRaises(DeserializationError):
            jsons.loadb('{"key": "value"}')
