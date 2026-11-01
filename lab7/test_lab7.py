import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout

from can_be_shipped import CanBeShipped
from digital_product import DigitalProduct
from inventory import Inventory
from inventory_file import InventoryFile
from physical_product import PhysicalProduct
from product import Product
from subscription_product import SubscriptionProduct


def capture_display(product):
    # Returns what display_information() prints.
    output = io.StringIO()
    with redirect_stdout(output):
        product.display_information()
    return output.getvalue()


class TestLab7(unittest.TestCase):
    # Section 7: Testing and review checklist.

    def setUp(self):
        self.physical = PhysicalProduct("P001", "Guitar", 350.00, 5, 3.2)
        self.digital = DigitalProduct("D001", "Operating System", 139.99, 100, 4500)

    def test_physical_stores_and_displays_weight(self):
        self.assertEqual(self.physical.get_weight(), 3.2)
        output = capture_display(self.physical)
        self.assertIn("ID: P001 | Name: Guitar | Price: $350.00 | Stock: 5", output)  # from parent
        self.assertIn("Weight: 3.20 kg", output)  # from child

    def test_digital_stores_and_displays_download_size(self):
        self.assertEqual(self.digital.get_download_size(), 4500.0)
        output = capture_display(self.digital)
        self.assertIn("ID: D001 | Name: Operating System", output)  # from parent
        self.assertIn("Download Size: 4500.00 MB", output)  # from child

    def test_both_subclasses_implement_fulfilment_info(self):
        self.assertIn("physical shipping", self.physical.get_fulfilment_info())
        self.assertIn("delivered digitally", self.digital.get_fulfilment_info())

    def test_abstract_product_cannot_be_instantiated(self):
        with self.assertRaises(TypeError):
            Product("X001", "Generic", 1.00, 1)

    def test_physical_products_calculate_shipping_cost(self):
        self.assertIsInstance(self.physical, CanBeShipped)
        light = PhysicalProduct("P002", "Pick", 1.00, 1, 0.0)
        heavy = PhysicalProduct("P003", "Amp", 500.00, 1, 20.0)
        self.assertEqual(light.calculate_shipping_cost(), 5.00)
        self.assertEqual(heavy.calculate_shipping_cost(), 55.00)
        self.assertEqual(self.physical.calculate_shipping_cost(), 13.00)

    def test_digital_products_do_not_need_shipping(self):
        self.assertNotIsInstance(self.digital, CanBeShipped)
        self.assertFalse(hasattr(self.digital, "calculate_shipping_cost"))

    def test_inventory_operations_still_work(self):
        inventory = Inventory()
        self.assertTrue(inventory.add_product(self.physical))
        self.assertTrue(inventory.add_product(self.digital))
        self.assertFalse(inventory.add_product(PhysicalProduct("P001", "Dup", 1, 1, 1)))
        self.assertIs(inventory.search_product("D001"), self.digital)
        self.assertIsNone(inventory.search_product("NOPE"))
        self.assertTrue(inventory.search_product("P001").update_stock(9))
        self.assertEqual(self.physical.get_stock(), 9)
        self.assertFalse(self.physical.update_stock(-1))
        self.assertEqual(len(inventory.get_all_products()), 2)

    def test_json_save_and_load_preserve_types(self):
        inventory = Inventory()
        inventory.add_product(self.physical)
        inventory.add_product(self.digital)
        inventory.add_product(SubscriptionProduct("S001", "Cloud Storage", 9.99, 50, 12))

        with tempfile.TemporaryDirectory() as folder:
            file_name = os.path.join(folder, "test_inventory.json")
            with redirect_stdout(io.StringIO()):
                InventoryFile(file_name).save(inventory)
                loaded = InventoryFile(file_name).load()

        physical = loaded.search_product("P001")
        digital = loaded.search_product("D001")
        subscription = loaded.search_product("S001")

        self.assertIsInstance(physical, PhysicalProduct)
        self.assertEqual(physical.get_weight(), 3.2)
        self.assertEqual(physical.get_price(), 350.00)
        self.assertIsInstance(digital, DigitalProduct)
        self.assertEqual(digital.get_download_size(), 4500.0)
        self.assertEqual(digital.get_stock(), 100)
        self.assertIsInstance(subscription, SubscriptionProduct)
        self.assertEqual(subscription.get_billing_months(), 12)

    def test_saved_json_has_type_identifier(self):
        self.assertEqual(self.physical.to_dict()["type"], "physical")
        self.assertEqual(self.digital.to_dict()["type"], "digital")


if __name__ == "__main__":
    unittest.main(verbosity=2)
