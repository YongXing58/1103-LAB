from digital_product import DigitalProduct
from physical_product import PhysicalProduct
from product import Product

# Walks through Sections 1-4 of Lab 7 from external code.

print("=== 1.2 / 2.2 PhysicalProduct ===")
guitar = PhysicalProduct("P100", "Acoustic Guitar", 350.00, 5, 3.2)
guitar.display_information()

print("\n=== 1.3 / 2.2 DigitalProduct ===")
os_licence = DigitalProduct("D100", "Operating System", 139.99, 100, 4500)
os_licence.display_information()

print("\n=== 3.2 get_fulfilment_info() ===")
print("Guitar: " + guitar.get_fulfilment_info())
print("OS:     " + os_licence.get_fulfilment_info())

print("\n=== 3.3 Instantiating abstract Product ===")
try:
    Product("X001", "Generic", 1.00, 1)
except TypeError as error:
    print("TypeError: " + str(error))

print("\n=== 4.2 calculate_shipping_cost() for different weights ===")
for weight in [0.5, 2.0, 10.0, 25.0]:
    item = PhysicalProduct("S" + str(weight), "Box", 10.00, 1, weight)
    print(format(weight, ">5.1f") + " kg -> $" + format(item.calculate_shipping_cost(), ".2f"))

print("\nDigitalProduct has calculate_shipping_cost()? "
      + str(hasattr(os_licence, "calculate_shipping_cost")))
