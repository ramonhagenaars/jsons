from unittest import TestCase

import jsons
from jsons import ValidationError


class C:
    def __init__(self, x: int):
        self.x = x


class TestValidation(TestCase):

    def test_validation_valid(self):
        jsons.set_validator(lambda c: c.x > 5, C)
        jsons.load({'x': 6}, C)  # Should be fine.

    def test_validation_invalid(self):
        jsons.set_validator(lambda c: c.x > 5, C)
        with self.assertRaises(ValidationError):
            jsons.load({'x': 3}, C)

    def test_validation_with_assert(self):

        def validator(c: C):
            assert c.x > 5  # A validator that raises.
            return True

        jsons.set_validator(validator, C)
        with self.assertRaises(ValidationError):
            jsons.load({'x': 3}, C)

    def test_validation_with_raise(self):

        def validator(c: C):
            if c.x <= 5:
                raise Exception('Not good...')
            return True

        jsons.set_validator(validator, C)

        try:
            jsons.load({'x': 3}, C)
        except ValidationError as err:
            self.assertEqual('Not good...', err.message)

    def test_validate_primitive_attribute_invalid(self):
        jsons.set_validator(lambda x: x == 1, int)
        with self.assertRaises(ValidationError):
            jsons.load({'x': 3}, C)

    def test_validate_primitive_attribute_valid(self):
        jsons.set_validator(lambda x: x == 1, int)
        jsons.load({'x': 1}, C)

    def test_validate_sequence(self):
        jsons.set_validator(lambda _: False, [int, str])
        with self.assertRaises(ValidationError):
            jsons.load({'x': 1}, C)

    def tearDown(self) -> None:
        jsons.set_validator(lambda _: True, C)
        jsons.set_validator(lambda _: True, int)
        jsons.set_validator(lambda _: True, str)
