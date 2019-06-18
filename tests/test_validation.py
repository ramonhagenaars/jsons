from unittest import TestCase
import jsons
from jsons import ValidationError


class TestValidation(TestCase):
    def test_validation(self):

        class C:
            def __init__(self, x: int):
                self.x = x

        jsons.set_validator(lambda c: c.x > 5, C)
        jsons.load({'x': 6}, C)  # Should be fine.
        with self.assertRaises(ValidationError):
            jsons.load({'x': 3}, C)

        def validator(c: C):
            assert c.x > 5
            return True

        jsons.set_validator(validator, C)
        with self.assertRaises(ValidationError):
            jsons.load({'x': 3}, C)

        def validator(c: C):
            if c.x <= 5:
                raise Exception('Not good...')
            return True

        jsons.set_validator(validator, C)
        try:
            jsons.load({'x': 3}, C)
        except ValidationError as err:
            self.assertEqual('Not good...', err.message)

        jsons.set_validator(lambda _: True, C)
        jsons.set_validator(lambda x: x == 1, int)
        with self.assertRaises(ValidationError):
            jsons.load({'x': 3}, C)
