from unittest import TestCase

import jsons

try:
    from jsons import *
except TypeError as error:
    _wildcard_import_error = str(error)
else:
    _wildcard_import_error = None


class TestWildcardImport(TestCase):
    def test_wildcard_import_exports_zoneinfo_handlers(self):
        assert _wildcard_import_error is None, _wildcard_import_error
        if jsons.default_zone_info_serializer and jsons.default_zone_info_deserializer:
            assert (globals().get('default_zone_info_serializer')
                    is jsons.default_zone_info_serializer)
            assert (globals().get('default_zone_info_deserializer')
                    is jsons.default_zone_info_deserializer)
