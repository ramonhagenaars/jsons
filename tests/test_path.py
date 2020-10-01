import os.path
from pathlib import Path, PureWindowsPath, PurePosixPath
from unittest import TestCase

import jsons


class TestPath(TestCase):

    def test_dump_singlepart_relative_path(self):
        self.assertEqual('abc', jsons.dump(Path('abc')))

    def test_dump_singlepart_pure_windows_path(self):
        self.assertEqual('abc', jsons.dump(PureWindowsPath('abc')))

    def test_dump_singlepart_pure_posix_path(self):
        self.assertEqual('abc', jsons.dump(PurePosixPath('abc')))

    def test_dump_multipart_relative_path(self):
        self.assertEqual(
            'abc/def/ghi',
            jsons.dump(Path('abc', 'def', 'ghi'))
        )
        self.assertEqual(
            'abc/def/ghi',
            jsons.dump(Path('abc/def/ghi'))
        )

    def test_dump_multipart_pure_windows_path(self):
        self.assertEqual(
            'abc/def/ghi',
            jsons.dump(PureWindowsPath('abc', 'def', 'ghi'))
        )
        self.assertEqual(
            'abc/def/ghi',
            jsons.dump(PureWindowsPath('abc/def/ghi'))
        )
        self.assertEqual(
            'abc/def/ghi',
            jsons.dump(PureWindowsPath('abc\\def\\ghi'))
        )

    def test_dump_multipart_pure_posix_path(self):
        self.assertEqual(
            'abc/def/ghi',
            jsons.dump(PurePosixPath('abc', 'def', 'ghi'))
        )
        self.assertEqual(
            'abc/def/ghi',
            jsons.dump(PurePosixPath('abc/def/ghi'))
        )
        self.assertEqual(
            'abc\\def\\ghi',
            jsons.dump(PurePosixPath('abc\\def\\ghi'))
        )

    def test_dump_multipart_drived_pure_windows_path(self):
        self.assertEqual(
            'Z:/abc/def/ghi',
            jsons.dump(PureWindowsPath('Z:\\', 'abc', 'def', 'ghi'))
        )
        self.assertEqual(
            'Z:/abc/def/ghi',
            jsons.dump(PureWindowsPath('Z:/abc/def/ghi'))
        )
        self.assertEqual(
            'Z:/abc/def/ghi',
            jsons.dump(PureWindowsPath('Z:\\abc\\def\\ghi'))
        )

    def test_dump_multipart_drived_pure_posix_path(self):
        self.assertEqual(
            'Z:/abc/def/ghi',
            jsons.dump(PurePosixPath('Z:', 'abc', 'def', 'ghi'))
        )
        self.assertEqual(
            'Z:/abc/def/ghi',
            jsons.dump(PurePosixPath('Z:/abc/def/ghi'))
        )
        self.assertEqual(
            'Z:\\abc\\def\\ghi',
            jsons.dump(PurePosixPath('Z:\\abc\\def\\ghi'))
        )

    #################

    def test_load_singlepart_relative_path(self):
        self.assertEqual(
            Path('abc'),
            jsons.load('abc', Path)
        )

    def test_load_singlepart_pure_windows_path(self):
        self.assertEqual(
            PureWindowsPath('abc'),
            jsons.load('abc', PureWindowsPath)
        )

    def test_load_singlepart_pure_posix_path(self):
        self.assertEqual(
            PurePosixPath('abc'),
            jsons.load('abc', PurePosixPath)
        )

    def test_load_multipart_relative_path(self):
        self.assertEqual(
            Path('abc', 'def', 'ghi'),
            jsons.load('abc/def/ghi', Path)
        )
        self.assertEqual(
            Path('abc/def/ghi'),
            jsons.load('abc/def/ghi', Path)
        )

    def test_load_multipart_pure_windows_path(self):
        # We should be able to load Posix-style paths on Windows.
        self.assertEqual(
            PureWindowsPath('abc', 'def', 'ghi'),
            jsons.load('abc/def/ghi', PureWindowsPath)
        )
        self.assertEqual(
            PureWindowsPath('abc/def/ghi'),
            jsons.load('abc/def/ghi', PureWindowsPath)
        )
        self.assertEqual(
            PureWindowsPath('abc\\def\\ghi'),
            jsons.load('abc/def/ghi', PureWindowsPath)
        )
        # We should be able to load Windows-style paths on Windows.
        self.assertEqual(
            PureWindowsPath('abc', 'def', 'ghi'),
            jsons.load('abc\\def\\ghi', PureWindowsPath)
        )
        self.assertEqual(
            PureWindowsPath('abc/def/ghi'),
            jsons.load('abc\\def\\ghi', PureWindowsPath)
        )
        self.assertEqual(
            PureWindowsPath('abc\\def\\ghi'),
            jsons.load('abc\\def\\ghi', PureWindowsPath)
        )

    def test_load_multipart_pure_posix_path(self):
        # We should be able to load Posix-style paths on Posix systems.
        self.assertEqual(
            PurePosixPath('abc', 'def', 'ghi'),
            jsons.load('abc/def/ghi', PurePosixPath)
        )
        self.assertEqual(
            PurePosixPath('abc/def/ghi'),
            jsons.load('abc/def/ghi', PurePosixPath)
        )
        self.assertNotEqual(
            PurePosixPath('abc\\def\\ghi'),
            jsons.load('abc/def/ghi', PurePosixPath)
        )
        # Backslashes on Posix systems should be interpreted as escapes.
        self.assertNotEqual(
            PurePosixPath('abc', 'def', 'ghi'),
            jsons.load('abc\\def\\ghi', PurePosixPath)
        )
        self.assertNotEqual(
            PurePosixPath('abc/def/ghi'),
            jsons.load('abc\\def\\ghi', PurePosixPath)
        )
        self.assertEqual(
            PurePosixPath('abc\\def\\ghi'),
            jsons.load('abc\\def\\ghi', PurePosixPath)
        )

    def test_load_multipart_drived_pure_windows_path(self):
        # We should be able to load Posix-style paths on Windows.
        self.assertEqual(
            PureWindowsPath('Z:\\', 'abc', 'def', 'ghi'),
            jsons.load('Z:/abc/def/ghi', PureWindowsPath)
        )
        self.assertEqual(
            PureWindowsPath('Z:/abc/def/ghi'),
            jsons.load('Z:/abc/def/ghi', PureWindowsPath)
        )
        self.assertEqual(
            PureWindowsPath('Z:\\abc\\def\\ghi'),
            jsons.load('Z:/abc/def/ghi', PureWindowsPath)
        )
        # We should be able to load Windows-style paths on Windows.
        self.assertEqual(
            PureWindowsPath('Z:\\', 'abc', 'def', 'ghi'),
            jsons.load('Z:\\abc\\def\\ghi', PureWindowsPath)
        )
        self.assertEqual(
            PureWindowsPath('Z:/abc/def/ghi'),
            jsons.load('Z:\\abc\\def\\ghi', PureWindowsPath)
        )
        self.assertEqual(
            PureWindowsPath('Z:\\abc\\def\\ghi'),
            jsons.load('Z:\\abc\\def\\ghi', PureWindowsPath)
        )

    def test_load_multipart_drived_pure_posix_path(self):
        # We should be able to load Posix-style paths on Windows.
        self.assertEqual(
            PurePosixPath('Z:', 'abc', 'def', 'ghi'),
            jsons.load('Z:/abc/def/ghi', PurePosixPath)
        )
        self.assertEqual(
            PurePosixPath('Z:/abc/def/ghi'),
            jsons.load('Z:/abc/def/ghi', PurePosixPath)
        )
        self.assertNotEqual(
            PurePosixPath('Z:\\abc\\def\\ghi'),
            jsons.load('Z:/abc/def/ghi', PurePosixPath)
        )
        # Backslashes on Posix systems should be interpreted as escapes.
        self.assertNotEqual(
            PurePosixPath('Z:', 'abc', 'def', 'ghi'),
            jsons.load('Z:\\abc\\def\\ghi', PurePosixPath)
        )
        self.assertNotEqual(
            PurePosixPath('Z:/abc/def/ghi'),
            jsons.load('Z:\\abc\\def\\ghi', PurePosixPath)
        )
        self.assertEqual(
            PurePosixPath('Z:\\abc\\def\\ghi'),
            jsons.load('Z:\\abc\\def\\ghi', PurePosixPath)
        )

    def test_dump_posix_load_windows(self):
        dump_result = jsons.dump(PurePosixPath('abc', 'def', 'ghi'))
        self.assertEqual(
            'abc/def/ghi',
            dump_result
        )
        load_result = jsons.load(dump_result, PureWindowsPath)
        self.assertEqual(
            PureWindowsPath('abc', 'def', 'ghi'),
            load_result
        )

    def test_dump_windows_load_posix(self):
        dump_result = jsons.dump(PureWindowsPath('abc', 'def', 'ghi'))
        self.assertEqual(
            'abc/def/ghi',
            dump_result
        )
        load_result = jsons.load(dump_result, PurePosixPath)
        self.assertEqual(
            PurePosixPath('abc', 'def', 'ghi'),
            load_result
        )

    def test_dump_posix_load_posix(self):
        dump_result = jsons.dump(PurePosixPath('abc', 'def', 'ghi'))
        self.assertEqual(
            'abc/def/ghi',
            dump_result
        )
        load_result = jsons.load(dump_result, PurePosixPath)
        self.assertEqual(
            PurePosixPath('abc', 'def', 'ghi'),
            load_result
        )

    def test_dump_windows_load_windows(self):
        dump_result = jsons.dump(PureWindowsPath('abc', 'def', 'ghi'))
        self.assertEqual(
            'abc/def/ghi',
            dump_result
        )
        load_result = jsons.load(dump_result, PureWindowsPath)
        self.assertEqual(
            PureWindowsPath('abc', 'def', 'ghi'),
            load_result
        )
