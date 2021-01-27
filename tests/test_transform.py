from unittest import TestCase

from jsons._transform_impl import transform


class TestTransform(TestCase):
    def test_transform(self):
        class A:
            def __init__(self, x: int):
                self.x = x

        class B:
            def __init__(self, x: str):
                self.x = x

        a = A(42)

        # Transform the key x to y and back to x.
        b = transform(a, B,
                      dump_kwargs={'key_transformer': lambda _: 'y'},
                      key_transformer=lambda _: 'x')

        self.assertIsInstance(b, B)
        self.assertEqual('42', b.x)

    def test_transform_with_mapper(self):
        class A:
            def __init__(self, x: int):
                self.x = x

        class B:
            def __init__(self, x: str, y: str):
                self.x = x
                self.y = y

        a = A(42)
        b = transform(a, B, mapper=lambda obj: {'y': obj['x'] + 1, **obj})

        self.assertIsInstance(b, B)
        self.assertEqual('42', b.x)
        self.assertEqual('43', b.y)
