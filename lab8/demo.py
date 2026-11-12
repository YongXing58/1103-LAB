from digital_product import DigitalProduct
from inventory import Inventory
from order import Order
from physical_product import PhysicalProduct
from product import Product
from supplier import Supplier

# Walks through Lab 8: association, aggregation, composition, LSP
# and polymorphism.


def show_product_details(product: Product) -> None:
    # Works with ANY Product - it never asks which subclass it is.
    product.display_information()
    print("    " + product.get_fulfilment_info())


print("=== 2. Association: Supplier and Product ===")
supplier = Supplier("SUP01", "Acme Supplies", "sales@acme.com")
guitar = PhysicalProduct("P001", "Acoustic Guitar", 350.00, 5, supplier, 3.2)
editor = DigitalProduct("D001", "Photo Editor", 59.90, 250, supplier, 850)
guitar.supplier.display_information()
editor.supplier.display_information()

print("\nDeleting the supplier variable (del supplier)...")
del supplier
guitar.supplier.display_information()
editor.supplier.display_information()
print("Products still have their supplier? " + str(guitar.supplier is editor.supplier))

print("\n=== 3. Aggregation: Inventory and Product ===")
inventory_a = Inventory()
inventory_b = Inventory()
inventory_a.add_product(guitar)
print("Inventory A has P001? " + str(inventory_a.find_product("P001") is guitar))
inventory_a.remove_product("P001")
print("Inventory A has P001 after remove? " + str(inventory_a.find_product("P001") is not None))
print("Product still works after removal:")
guitar.display_information()
inventory_b.add_product(guitar)
print("Same object added to Inventory B? " + str(inventory_b.find_product("P001") is guitar))

print("\n=== 4. Composition: Order and OrderLine ===")
order_1 = Order("O001")
order_1.add_order_line(guitar, 2)
order_1.add_order_line(editor, 1)
order_1.display_order()

order_2 = Order("O002")
order_2.add_order_line(guitar, 1)
print("\nSame Product in two orders:")
print("Same Product object? " + str(order_1.order_lines[0].product is order_2.order_lines[0].product))
print("Same OrderLine object? " + str(order_1.order_lines[0] is order_2.order_lines[0]))

order_1.remove_order_line("D001")
print("\nAfter removing the digital line from order O001:")
order_1.display_order()

print("\n=== 6 & 7. LSP and polymorphism through Product ===")
inventory = Inventory()
inventory.add_product(guitar)
inventory.add_product(editor)
for product in inventory.get_all_products():
    show_product_details(product)
