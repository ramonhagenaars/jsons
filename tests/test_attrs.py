import sys
from unittest import TestCase, skipIf

import jsons
from jsons import DeserializationError
try:
    from test_resources.attrs_classes import (
        AttrsClass,
        AttrsClassAutoAttribs,
        AttrsClassPrivate,
        AttrsClassPrivateAndDunder,
        AttrsClassDefault,
        AttrsClassValidator,
        AttrsClassConverter,
        AttrsClassNoInit,
        AttrsClassNoInitSome,
        AttrsClassFrozen,
        AttrsClassSlots,
        AttrsClassKwOnly,
    )
except ImportError:
    pass  # In case of 3.5


@skipIf(sys.version_info.minor == 5, reason='Unsupported syntax for 3.5')
class TestAttrs(TestCase):
    def test_dump(self):
        c = AttrsClass('test', 42)

        dumped = jsons.dump(c)

        self.assertEqual({'a': 'test', 'b': 42}, dumped)

    def test_load(self):
        loaded = jsons.load({'a': 'test', 'b': 42}, AttrsClass)

        self.assertEqual('test', loaded.a)
        self.assertEqual(42, loaded.b)

    def test_dump_auto_attribs(self):
        c = AttrsClassAutoAttribs('test', 42)

        dumped = jsons.dump(c)

        self.assertEqual({'a': 'test', 'b': 42}, dumped)

    def test_load_auto_attribs(self):
        loaded = jsons.load({'a': 'test', 'b': 42}, AttrsClassAutoAttribs)

        self.assertEqual('test', loaded.a)
        self.assertEqual(42, loaded.b)

    def test_dump_private(self):
        c = AttrsClassPrivate('private')

        dumped = jsons.dump(c)

        self.assertEqual({'a': 'private'}, dumped)

    def test_load_private(self):
        loaded = jsons.load({'a': 'private', 'b__': 'dunder'}, AttrsClassPrivateAndDunder)

        self.assertEqual('private', loaded._a)
        self.assertEqual('dunder', loaded.__b__)

    def test_load_defaults(self):
        loaded = jsons.load({}, AttrsClassDefault)

        self.assertEqual('standard', loaded.a)

    def test_load_with_validator(self):
        loaded = jsons.load({'a': 9}, AttrsClassValidator)

        self.assertEqual(9, loaded.a)

        with self.assertRaises(DeserializationError) as err:
            jsons.load({'a': 11}, AttrsClassValidator)

        self.assertIn('Cannot be greater than 10', str(err.exception))

    def test_load_with_converter(self):
        loaded = jsons.load({'a': '42', 'b': '43'}, AttrsClassConverter)

        self.assertEqual(42, loaded.a)

        # attr will have the final word: b should be an int.
        self.assertEqual(43, loaded.b)

    def test_load_without_init(self):
        loaded = jsons.load({'a': 42}, AttrsClassNoInit)

        self.assertEqual(42, loaded.a)

    def test_load_without_init_for_some(self):
        loaded = jsons.load({'a': 42, 'b': '43'}, AttrsClassNoInitSome)

        self.assertEqual(42, loaded.a)
        self.assertEqual('43', loaded.b)

    def test_load_frozen(self):
        loaded = jsons.load({'a': 42}, AttrsClassFrozen)

        self.assertEqual(42, loaded.a)

    def test_load_slots(self):
        loaded = jsons.load({'a': 42}, AttrsClassSlots)

        self.assertEqual(42, loaded.a)

    def test_load_kw_only(self):
        loaded = jsons.load({'a': 42}, AttrsClassKwOnly)

        self.assertEqual(42, loaded.a)
