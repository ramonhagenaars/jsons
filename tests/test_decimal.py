from decimal import Decimal
from unittest import TestCase
import jsons


class TestDecimal(TestCase):
    def test_dump_decimal(self):
        self.assertEqual('12.345', jsons.dump(Decimal('12.345')))
        self.assertEqual('2.5', jsons.dump(Decimal(2.5)))
        self.assertEqual('25', jsons.dump(Decimal(25)))

    def test_load_decimal(self):
        self.assertEqual(Decimal('12.345'), jsons.load('12.345', Decimal))
        self.assertEqual(Decimal(2.5), jsons.load(2.5, Decimal))
        self.assertEqual(Decimal(25), jsons.load(25, Decimal))
