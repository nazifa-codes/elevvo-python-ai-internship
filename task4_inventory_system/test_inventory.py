import unittest
from datetime import date
from inventory import Inventory, Product, PerishableProduct


class InventoryTests(unittest.TestCase):
    def test_stock_validation(self):
        product = Product("A1", "Pen", 5)
        with self.assertRaises(ValueError):
            product.stock = -1

    def test_add_and_remove_stock(self):
        product = Product("A1", "Pen", 5)
        product.add_stock(3)
        product.remove_stock(2)
        self.assertEqual(product.stock, 6)

    def test_cannot_remove_more_than_available(self):
        product = Product("A1", "Pen", 2)
        with self.assertRaises(ValueError):
            product.remove_stock(3)

    def test_perishable_expiry_behavior(self):
        milk = PerishableProduct("M1", "Milk", 3, "2026-01-01")
        self.assertTrue(milk.is_expired(date(2026, 2, 1)))
        self.assertIn("EXPIRED", milk.report_line())

    def test_inventory_alert_and_report(self):
        inventory = Inventory()
        product = Product("A1", "Pen", 2, reorder_level=5)
        inventory.add_product(product)
        self.assertEqual(len(inventory.get_low_stock_alerts()), 1)
        self.assertIn("Pen", inventory.generate_report())


if __name__ == "__main__":
    unittest.main()
