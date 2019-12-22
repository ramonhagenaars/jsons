import datetime
from unittest import TestCase

import jsons
from jsons import DeserializationError


class WrongUser:
    def __init__(self,
                 id: int,
                 birthday: datetime,  # intentionally wrong
    ):
        self.id = id
        self.birthday = birthday


class CorrectUser:
    def __init__(self,
                 id: int,
                 birthday: datetime.datetime,
    ):
        self.id = id
        self.birthday = birthday


class TestTypeError(TestCase):
    def test_undefined_deserializer(self):
        dumped = {'id': 12, 'birthday': '1879-03-14T11:30:00+01:00'}
        with self.assertRaises(DeserializationError) as errorContext:
            jsons.load(dumped, WrongUser)
        error = errorContext.exception
        self.assertEqual('No deserializer for type "datetime"', error.message)
        self.assertEqual(datetime, error.target)

    def test_wrong_primitive_type(self):
        dumped = {'id': 'Albert', 'birthday': '1879-03-14T11:30:00+01:00'}
        with self.assertRaises(DeserializationError) as errorContext:
            jsons.load(dumped, WrongUser)
        error = errorContext.exception
        self.assertEqual('Could not cast "Albert" into "int"', error.message)
        self.assertEqual(int, error.target)

    def test_wrong_type(self):
        dumped = {'id': 12, 'birthday': 'every day'}
        with self.assertRaises(DeserializationError) as errorContext:
            jsons.load(dumped, CorrectUser)
        error = errorContext.exception
        self.assertTrue(error.message.startswith('Could not deserialize value "every day" into "datetime.datetime".'))
        self.assertEqual(datetime.datetime, error.target)
