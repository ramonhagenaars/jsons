import datetime
from dataclasses import dataclass
from unittest import TestCase
import jsons
from jsons import DeserializationError


@dataclass
class WrongUser:
    id: int
    birthday: datetime  # intentionally wrong


@dataclass
class CorrectUser:
    id: int
    birthday: datetime.datetime


class TestTypeError(TestCase):
    def test_undefined_deserializer(self):
        dumped = {'id': 12, 'birthday': '1879-03-14T11:30:00+01:00'}
        with self.assertRaises(DeserializationError) as errorContext:
            jsons.load(dumped, WrongUser)
        error: DeserializationError = errorContext.exception
        self.assertEqual('No deserializer for type "datetime"', error.message)
        self.assertEqual(datetime, error.target)

    def test_wrong_primitive_type(self):
        dumped = {'id': 'Albert', 'birthday': '1879-03-14T11:30:00+01:00'}
        with self.assertRaises(DeserializationError) as errorContext:
            jsons.load(dumped, WrongUser)
        error: DeserializationError = errorContext.exception
        self.assertEqual('Could not cast "Albert" into "int"', error.message)
        self.assertEqual(int, error.target)

    def test_wrong_type(self):
        dumped = {'id': 12, 'birthday': 'every day'}
        with self.assertRaises(DeserializationError) as errorContext:
            jsons.load(dumped, CorrectUser)
        error: DeserializationError = errorContext.exception
        self.assertTrue(error.message.startswith('Could not deserialize value "every day" into "datetime.datetime".'))
        self.assertEqual(datetime.datetime, error.target)
