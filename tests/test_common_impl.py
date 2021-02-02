from unittest import TestCase

from jsons._common_impl import get_class_name, get_cls_from_str


class TestCommonImpl(TestCase):
    def test_get_class_name_without__name__(self):

        class Meta(type):
            __name__ = None

        class C(metaclass=Meta):
            pass

        self.assertEqual('C', get_class_name(C))
        self.assertEqual('{}.C'.format(__name__),
                         get_class_name(C, fully_qualified=True))

    def test_get_class_name_of_none(self):
        self.assertEqual('NoneType', get_class_name(None))

    def test_get_cls_from_str(self):
        self.assertEqual(str, get_cls_from_str('str', {}, None))
        self.assertEqual(int, get_cls_from_str('int', {}, None))
        self.assertEqual(list, get_cls_from_str('list', {}, None))
