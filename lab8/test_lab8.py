import io
import unittest
from contextlib import redirect_stdout

from can_be_shipped import CanBeShipped
from digital_product import DigitalProduct
from inventory import Inventory
from order import Order
from order_line import OrderLine
from physical_product import PhysicalProduct
from product import Product
from supplier import Supplier


def capture(function) -> str:
    # Returns what a function prints.
    output = io.StringIO()
    with redirect_stdout(output):
        function()
    return output.getvalue()


def show_product_details(product: Product) -> None:
    # Accepts any Product and only uses what every Product supports.
    product.display_information()
    print(product.get_fulfilment_info())


class TestLab8(unittest.TestCase):
    # Section 9: Testing and review checklist.

    def setUp(self):
        self.supplier = Supplier("SUP01", "Acme Supplies", "sales@acme.com")
        self.physical = PhysicalProduct("P001", "Guitar", 350.00, 5, self.supplier, 3.2)
        self.digital = DigitalProduct("D001", "Photo Editor", 59.90, 250, self.supplier, 850)

    # --- Association: Supplier and Product ---

    def test_product_stores_reference_to_its_supplier(self):
        self.assertIs(self.physical.supplier, self.supplier)
        self.assertIs(self.digital.supplier, self.supplier)

    def test_supplier_and_product_exist_independently(self):
        supplier = self.supplier
        product = self.physical
        del supplier  # deleting one name does not destroy the object
        self.assertIn("Acme Supplies", capture(product.supplier.display_information))

    # --- Aggregation: Inventory and Product ---

    def test_inventory_aggregates_products(self):
        inventory = Inventory()
        inventory.add_product(self.physical)
        inventory.add_product(self.digital)
        self.assertEqual(len(inventory.get_all_products()), 2)
        self.assertIs(inventory.find_product("P001"), self.physical)
        self.assertIsNone(inventory.find_product("X999"))

    def test_product_survives_removal_and_moves_to_another_inventory(self):
        inventory_a = Inventory()
        inventory_b = Inventory()
        inventory_a.add_product(self.physical)

        self.assertTrue(inventory_a.remove_product("P001"))
        self.assertIsNone(inventory_a.find_product("P001"))
        self.assertEqual(self.physical.get_name(), "Guitar")  # still usable

        inventory_b.add_product(self.physical)
        self.assertIs(inventory_b.find_product("P001"), self.physical)

    # --- Composition: Order and OrderLine ---

    def test_order_creates_and_manages_its_order_lines(self):
        order = Order("O001")
        order.add_order_line(self.physical, 2)
        self.assertEqual(len(order.order_lines), 1)
        self.assertIsInstance(order.order_lines[0], OrderLine)

    def test_order_line_refers_to_product_without_owning_it(self):
        order_1 = Order("O001")
        order_2 = Order("O002")
        order_1.add_order_line(self.physical, 1)
        order_2.add_order_line(self.physical, 1)

        self.assertIsNot(order_1.order_lines[0], order_2.order_lines[0])  # 2 lines
        self.assertIs(order_1.order_lines[0].product, order_2.order_lines[0].product)  # 1 product

    def test_order_calculates_total_from_order_lines(self):
        order = Order("O001")
        order.add_order_line(self.physical, 2)  # 700.00
        order.add_order_line(self.digital, 1)   # 59.90
        self.assertAlmostEqual(order.calculate_total(), 759.90)

    def test_removing_an_order_line_does_not_affect_the_product(self):
        order = Order("O001")
        order.add_order_line(self.physical, 1)
        self.assertTrue(order.remove_order_line("P001"))
        self.assertEqual(len(order.order_lines), 0)
        self.assertEqual(self.physical.get_price(), 350.00)

    # --- Type hints ---

    def test_type_hints_are_present(self):
        self.assertIs(Product.__init__.__annotations__["supplier"], Supplier)
        self.assertEqual(Inventory.add_product.__annotations__["product"], Product)
        self.assertEqual(Inventory.find_product.__annotations__["return"], Product | None)
        self.assertEqual(OrderLine.calculate_subtotal.__annotations__["return"], float)

    # --- LSP and polymorphism ---

    def test_show_product_details_works_with_both_subclasses(self):
        self.assertIn("physical shipping", capture(lambda: show_product_details(self.physical)))
        self.assertIn("delivered digitally", capture(lambda: show_product_details(self.digital)))

    def test_inventory_works_with_both_types_through_product(self):
        inventory = Inventory()
        inventory.add_product(self.physical)
        inventory.add_product(self.digital)
        output = capture(inventory.display_all_products)
        self.assertIn("Weight: 3.20 kg", output)
        self.assertIn("Download Size: 850.00 MB", output)

    def test_both_subclasses_preserve_update_stock_behaviour(self):
        for product in [self.physical, self.digital]:
            self.assertTrue(product.update_stock(10))
            self.assertEqual(product.get_stock(), 10)
            self.assertFalse(product.update_stock(-1))
            self.assertEqual(product.get_stock(), 10)

    def test_physical_is_shippable_digital_is_not(self):
        self.assertIsInstance(self.physical, CanBeShipped)
        self.assertNotIsInstance(self.digital, CanBeShipped)


if __name__ == "__main__":
    unittest.main()
