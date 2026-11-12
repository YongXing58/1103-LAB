import inspect
import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

import main
import order as order_module
from discount_strategy import (BulkDiscount, DiscountStrategy, NoDiscount,
                               PercentageDiscount, StudentDiscount)
from digital_product import DigitalProduct
from inventory import Inventory
from order import Order
from order_line import OrderLine
from physical_product import PhysicalProduct
from product_factory import ProductFactory
from product_loader import load_products
from supplier import Supplier

CSV_TEXT = """product_type,product_id,name,price,stock_quantity
physical,P001,Desk Lamp,25.00,10
digital,D001,Photo Editor,49.90,100
service,S001,Installation,30.00,5
physical,P002,Office Chair,abc,3
physical,P003,Monitor Stand,39.50,7
"""


class FlatTenDiscount(DiscountStrategy):
    # A brand new strategy written only in the test - Order is not edited.
    def apply(self, total: float) -> float:
        return total - 10


class TestLab9(unittest.TestCase):

    def setUp(self):
        self.supplier = Supplier("SUP01", "Acme Supplies", "sales@acme.com")
        self.product = ProductFactory.create("physical", "P001", "Lamp", 125.00, 10, self.supplier, 1.5)

    def make_order(self, discount=None) -> Order:
        order = Order("O001", discount)
        order.add_order_line(self.product, 2)  # total 250
        return order

    # --- Strategy ---

    def test_order_calculates_total_through_strategy(self):
        self.assertEqual(self.make_order(BulkDiscount(200, 20)).calculate_total(), 230)
        self.assertEqual(self.make_order(PercentageDiscount(10)).calculate_total(), 225)

    def test_order_defaults_to_no_discount(self):
        order = self.make_order()
        self.assertIsInstance(order.discount, NoDiscount)
        self.assertEqual(order.calculate_total(), 250)

    def test_bulk_discount_below_threshold_is_unchanged(self):
        self.assertEqual(BulkDiscount(200, 20).apply(150), 150)

    def test_new_strategy_works_without_changing_order(self):
        self.assertEqual(self.make_order(FlatTenDiscount()).calculate_total(), 240)
        self.assertAlmostEqual(self.make_order(StudentDiscount()).calculate_total(), 237.5)

    def test_set_discount_changes_strategy_on_existing_order(self):
        order = self.make_order(BulkDiscount(200, 20))
        self.assertEqual(order.calculate_total(), 230)
        order.set_discount(PercentageDiscount(10))
        self.assertEqual(order.calculate_total(), 225)

    def test_order_contains_no_discount_if_elif_logic(self):
        source = inspect.getsource(order_module.Order)
        self.assertNotIn("elif", source)

    # --- Factory ---

    def test_factory_returns_correct_product_types(self):
        digital = ProductFactory.create("digital", "D001", "Editor", 49.90, 5, self.supplier, 850)
        self.assertIsInstance(self.product, PhysicalProduct)
        self.assertIsInstance(digital, DigitalProduct)

    def test_products_are_created_through_factory_not_directly(self):
        import inventory_file
        import product_loader
        for module in (main, inventory_file, product_loader):
            source = inspect.getsource(module)
            self.assertNotIn("PhysicalProduct(", source)
            self.assertNotIn("DigitalProduct(", source)

    def test_factory_unknown_type_raises_clear_error(self):
        with self.assertRaises(ValueError) as context:
            ProductFactory.create("service", "S001", "Install", 30.00, 5, self.supplier)
        self.assertEqual(str(context.exception), "Unknown product type: service")

    # --- Validation ---

    def test_invalid_price_is_rejected(self):
        for bad_price in [0, -5]:
            with self.assertRaises(ValueError):
                ProductFactory.create("physical", "P9", "Bad", bad_price, 1, self.supplier)

    def test_negative_stock_is_rejected(self):
        with self.assertRaises(ValueError):
            ProductFactory.create("digital", "D9", "Bad", 10, -1, self.supplier)
        with self.assertRaises(ValueError):
            self.product.update_stock(-1)
        self.assertEqual(self.product.get_stock(), 10)

    def test_order_line_quantity_must_be_greater_than_zero(self):
        for bad_quantity in [0, -2]:
            with self.assertRaises(ValueError):
                OrderLine(self.product, bad_quantity)
        with self.assertRaises(ValueError):
            Order("O2").add_order_line(self.product, 0)

    # --- Exception handling: user input ---

    def test_get_positive_float_asks_again_until_valid(self):
        with patch("builtins.input", side_effect=["abc", "-5", "12.50"]):
            output = io.StringIO()
            with redirect_stdout(output):
                value = main.get_positive_float("Price: ")
        self.assertEqual(value, 12.5)
        self.assertIn("Please enter a valid number, e.g. 12.50", output.getvalue())
        self.assertIn("Please enter a number greater than zero.", output.getvalue())

    # --- Exception handling: files ---

    def run_load(self, path: str):
        inventory = Inventory()
        output = io.StringIO()
        with redirect_stdout(output):
            load_products(path, inventory, self.supplier)
        return inventory, output.getvalue()

    def test_missing_file_is_handled_gracefully(self):
        inventory, output = self.run_load("does_not_exist.csv")
        self.assertIn("Products file not found: does_not_exist.csv", output)
        self.assertIn("Load attempt finished.", output)
        self.assertNotIn("products loaded", output)
        self.assertEqual(len(inventory.get_all_products()), 0)

    def test_bad_rows_are_skipped_and_valid_rows_load(self):
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "products.csv")
            with open(path, "w", newline="") as f:
                f.write(CSV_TEXT)
            inventory, output = self.run_load(path)

        ids = [p.get_product_id() for p in inventory.get_all_products()]
        self.assertEqual(ids, ["P001", "D001", "P003"])
        self.assertIn("Unknown product type: service", output)
        self.assertIn("could not convert string to float", output)
        self.assertIn("3 products loaded.", output)
        self.assertTrue(output.rstrip().endswith("Load attempt finished."))


if __name__ == "__main__":
    unittest.main()
