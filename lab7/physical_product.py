from can_be_shipped import CanBeShipped
from product import Product


class PhysicalProduct(Product, CanBeShipped):
    # Responsibility: a product that exists physically and is shipped.
    # Inherits from Product (is-a) and implements the CanBeShipped
    # interface (must-be-able-to be shipped).

    PRODUCT_TYPE = "physical"

    # Simple shipping rule: flat base fee plus a cost per kilogram.
    BASE_SHIPPING_FEE = 5.00
    COST_PER_KG = 2.50

    def __init__(self, product_id, name, price, stock, weight):
        # Reuse the Product constructor for the common attributes.
        super().__init__(product_id, name, price, stock)
        self.__weight = float(weight)

    def get_weight(self):
        return self.__weight

    def display_information(self):
        # Overrides Product.display_information(): the parent prints
        # the common details, this class adds only what is unique to it.
        super().display_information()
        print("    Type: Physical | Weight: " + format(self.__weight, ".2f") + " kg")

    def get_fulfilment_info(self):
        return "This product requires physical shipping to the customer."

    def calculate_shipping_cost(self):
        return round(self.BASE_SHIPPING_FEE + self.__weight * self.COST_PER_KG, 2)

    def to_dict(self):
        data = super().to_dict()
        data["type"] = self.PRODUCT_TYPE
        data["weight"] = self.__weight
        return data

    @classmethod
    def from_dict(cls, data):
        return cls(data["id"], data["name"], data["price"], data["stock"], data["weight"])
