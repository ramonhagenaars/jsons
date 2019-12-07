import datetime
from dataclasses import dataclass
from unittest import TestCase
import jsons
from jsons import DeserializationError


@dataclass
class WrongUser:
    id: int
    birthday: datetime  # intentionally wrong


class TestTypeError(TestCase):
    def test_undefined_deserializer(self):
        dumped = {'id': 12, 'birthday': '1879-03-14T11:30:00+01:00'}
        with self.assertRaises(DeserializationError) as errorContext:
            jsons.load(dumped, WrongUser)
        error: DeserializationError = errorContext.exception
        self.assertEqual('No deserializer for type datetime', error.message)
        self.assertEqual(datetime, error.target)
