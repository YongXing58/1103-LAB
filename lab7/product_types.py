from digital_product import DigitalProduct
from physical_product import PhysicalProduct
from subscription_product import SubscriptionProduct

# Registry of every product type the system knows about.
# Responsibility: the ONE place that maps a type identifier (as saved
# in JSON) to its class, a menu label and the prompt for its extra
# attribute. Adding a new product type only needs a new class and one
# new line here - Inventory, InventoryFile and the menu stay unchanged.
#
# type id: (menu label, class, extra attribute prompt, extra value type)
PRODUCT_TYPES = {
    PhysicalProduct.PRODUCT_TYPE: ("Physical Product", PhysicalProduct, "Weight (kg): ", float),
    DigitalProduct.PRODUCT_TYPE: ("Digital Product", DigitalProduct, "Download Size (MB): ", float),
    SubscriptionProduct.PRODUCT_TYPE: ("Subscription Product", SubscriptionProduct, "Billing Period (months): ", int),
}


def get_product_class(product_type):
    # Returns the class for a type identifier, or None if unknown.
    entry = PRODUCT_TYPES.get(product_type)
    if entry is None:
        return None
    return entry[1]
