from digital_product import DigitalProduct
from physical_product import PhysicalProduct

# Registry of every product type the system knows about.
# Responsibility: the ONE place that maps a type identifier (as saved
# in JSON) to its class, a menu label and the prompt for its extra
# attribute.
#
# type id: (menu label, class, extra attribute prompt)
PRODUCT_TYPES: dict = {
    PhysicalProduct.PRODUCT_TYPE: ("Physical Product", PhysicalProduct, "Weight (kg): "),
    DigitalProduct.PRODUCT_TYPE: ("Digital Product", DigitalProduct, "Download Size (MB): "),
}


def get_product_class(product_type: str):
    # Returns the class for a type identifier, or None if unknown.
    entry = PRODUCT_TYPES.get(product_type)
    if entry is None:
        return None
    return entry[1]
