import sys
from unittest import TestCase, skipIf

import attr

import jsons
from jsons import DeserializationError


@skipIf(sys.version_info.minor == 5, reason='Unsupported syntax for 3.5')
class TestAttrs(TestCase):
    def test_dump(self):
        @attr.s
        class C:
            a: str = attr.ib()
            b: int = attr.ib()

        c = C('test', 42)

        dumped = jsons.dump(c)

        self.assertEqual({'a': 'test', 'b': 42}, dumped)

    def test_load(self):
        @attr.s
        class C:
            a: str = attr.ib()
            b: int = attr.ib()

        loaded = jsons.load({'a': 'test', 'b': 42}, C)

        self.assertEqual('test', loaded.a)
        self.assertEqual(42, loaded.b)

    def test_dump_auto_attribs(self):
        @attr.s(auto_attribs=True)
        class C:
            a: str
            b: int

        c = C('test', 42)

        dumped = jsons.dump(c)

        self.assertEqual({'a': 'test', 'b': 42}, dumped)

    def test_load_auto_attribs(self):
        @attr.s(auto_attribs=True)
        class C:
            a: str
            b: int

        loaded = jsons.load({'a': 'test', 'b': 42}, C)

        self.assertEqual('test', loaded.a)
        self.assertEqual(42, loaded.b)

    def test_dump_private(self):
        @attr.s
        class C:
            _a: str = attr.ib()

        c = C('private')

        dumped = jsons.dump(c)

        self.assertEqual({'a': 'private'}, dumped)

    def test_load_private(self):
        @attr.s
        class C:
            _a: str = attr.ib()
            __b__: str = attr.ib()

        loaded = jsons.load({'a': 'private', 'b__': 'dunder'}, C)

        self.assertEqual('private', loaded._a)
        self.assertEqual('dunder', loaded.__b__)

    def test_load_defaults(self):
        @attr.s
        class C:
            a: str = attr.ib(default='standard')

        loaded = jsons.load({}, C)

        self.assertEqual('standard', loaded.a)

    def test_load_with_validator(self):
        @attr.s
        class C:
            a: int = attr.ib()

            @a.validator
            def _check(self, attribute, value):
                if value > 10:
                    raise ValueError('Cannot be greater than 10')

        loaded = jsons.load({'a': 9}, C)

        self.assertEqual(9, loaded.a)

        with self.assertRaises(DeserializationError) as err:
            jsons.load({'a': 11}, C)

        self.assertIn('Cannot be greater than 10', str(err.exception))

    def test_load_with_converter(self):
        @attr.s
        class C:
            a: int = attr.ib(converter=int)
            b: str = attr.ib(converter=int)  # This gets weird.

        loaded = jsons.load({'a': '42', 'b': '43'}, C)

        self.assertEqual(42, loaded.a)

        # attr will have the final word: b should be an int.
        self.assertEqual(43, loaded.b)

    def test_load_without_init(self):
        @attr.s(init=False)
        class C:
            a: int = attr.ib()

        loaded = jsons.load({'a': 42}, C)

        self.assertEqual(42, loaded.a)

    def test_load_without_init_for_some(self):
        @attr.s
        class C:
            a: int = attr.ib()
            b: str = attr.ib(init=False)

        loaded = jsons.load({'a': 42, 'b': '43'}, C)

        self.assertEqual(42, loaded.a)
        self.assertEqual('43', loaded.b)

    def test_load_frozen(self):
        @attr.s(frozen=True)
        class C:
            a: int = attr.ib()

        loaded = jsons.load({'a': 42}, C)

        self.assertEqual(42, loaded.a)

    def test_load_slots(self):
        @attr.s(slots=True)
        class C:
            a: int = attr.ib()

        loaded = jsons.load({'a': 42}, C)

        self.assertEqual(42, loaded.a)

    def test_load_kw_only(self):
        @attr.s(kw_only=True)
        class C:
            a: int = attr.ib()

        loaded = jsons.load({'a': 42}, C)

        self.assertEqual(42, loaded.a)
