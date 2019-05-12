import sys
import uuid
from pathlib import Path
from typing import Any
from unittest import TestCase, skipUnless
import jsons
from jsons._compatibility_impl import get_type_hints
from jsons.exceptions import SignatureMismatchError

try:
    from dataclasses import dataclass
except ImportError:
    dataclass = None


# Load the test resources into the path, so they can be imported. They MUST
# remain outside of the tests package to prevent the test discovery from
# reading in them too soon.
path = Path(__file__).parent.parent.joinpath(Path('test_resources')).absolute()
sys.path.insert(0, str(path))


def only_version_3(minor_version: int, and_above: bool = False):
    def _decorator(decorated):
        dont_skip = (sys.version_info.minor >= minor_version if and_above
                     else minor_version == sys.version_info.minor)
        reason = 'Only 3.{}{}'.format(minor_version, '+' if and_above else '')

        @skipUnless(dont_skip, reason=reason)
        def _wrapper(*args, **kwargs):
            return decorated(*args, **kwargs)

        return _wrapper
    return _decorator


class TestSpecificVersions(TestCase):

    @only_version_3(7)
    def test_simple_dump_and_load_dataclass_with_future_import(self):
        import version_37
        from version_with_dataclasses import Person
        p = Person('John')
        dumped = jsons.dump(p)
        loaded = jsons.load(dumped, Person)
        self.assertEqual(p.name, loaded.name)

        with self.assertRaises(SignatureMismatchError):
            jsons.load({'name': 'John', 'age': 88}, Person, strict=True)

    @only_version_3(6, and_above=True)
    def test_simple_dump_and_load_dataclass(self):
        from version_with_dataclasses import Person
        p = Person('John')
        dumped = jsons.dump(p)
        loaded = jsons.load(dumped, Person)
        self.assertEqual(p.name, loaded.name)

        with self.assertRaises(SignatureMismatchError):
            jsons.load({'name': 'John', 'age': 88}, Person, strict=True)

    @only_version_3(6, and_above=True)
    def test_namedtuple_with_optional(self):
        from version_with_dataclasses import (
            NamedTupleWithOptional,
            NamedTupleWithUnion,
            NamedTupleWithAny
        )

        self.assertEqual(NamedTupleWithOptional(None),
                         jsons.load({'arg': None}, NamedTupleWithOptional))

        self.assertEqual(NamedTupleWithUnion(None),
                         jsons.load({'arg': None}, NamedTupleWithUnion))

        self.assertEqual(NamedTupleWithAny(123),
                         jsons.load({'arg': 123}, NamedTupleWithAny))

    @only_version_3(5, and_above=True)
    def test_simple_dump_and_load_dataclass(self):

        class C:
            pass

        hints = get_type_hints(C.__init__)
        self.assertDictEqual({}, hints)

    @only_version_3(6, and_above=True)
    def test_uuid_serialization(self):
        from version_with_dataclasses import User
        user = User(uuid.uuid4(), 'name')

        dumped = jsons.dump(user)
        self.assertEqual(dumped['user_uuid'], str(user.user_uuid))

        loaded = jsons.load(dumped, User)
        self.assertEqual(user.user_uuid, loaded.user_uuid)

        self.assertEqual('name', loaded.name)
