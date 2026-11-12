import builtins
from discount_strategy import BulkDiscount, PercentageDiscount, StudentDiscount
from inventory import Inventory
from main import get_positive_float
from order import Order
from product_factory import ProductFactory
from product_loader import load_products
from supplier import Supplier

# Walks through the Predict First scenarios of Lab 9.

supplier = Supplier("SUP01", "Acme Supplies", "sales@acme.com")

print("=== 2.3 Strategy: order total 250 ===")
lamp = ProductFactory.create("physical", "P001", "Desk Lamp", 125.00, 10, supplier, 1.5)
order = Order("O001", BulkDiscount(200, 20))
order.add_order_line(lamp, 2)
print("BulkDiscount(200, 20):      " + format(order.calculate_total(), ".2f"))
order.set_discount(PercentageDiscount(10))
print("PercentageDiscount(10):     " + format(order.calculate_total(), ".2f"))
order.set_discount(StudentDiscount())
print("StudentDiscount (new class): " + format(order.calculate_total(), ".2f"))

print("\n=== 3.2 Factory: unknown product type ===")
try:
    ProductFactory.create("service", "S001", "Installation", 30.00, 5, supplier)
except ValueError as error:
    print("ValueError: " + str(error))

print("\n=== 5.1 get_positive_float with inputs: abc, -5, 12.50 ===")
answers = iter(["abc", "-5", "12.50"])
real_input = builtins.input


def scripted_input(prompt):
    # Pretends the user typed the next answer: shows it, then returns it.
    text = next(answers)
    print(prompt + text)
    return text


builtins.input = scripted_input
value = get_positive_float("Price: ")
builtins.input = real_input
print("Returned: " + str(value))

print("\n=== 5.2 load_products with products.csv ===")
inventory = Inventory()
load_products("products.csv", inventory, supplier)
inventory.display_all_products()

print("\n=== 5.2 load_products with a missing file ===")
load_products("products_renamed.csv", Inventory(), supplier)
