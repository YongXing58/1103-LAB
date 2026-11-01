from product import Product


class SubscriptionProduct(Product):
    # Optional task (Section 8): a new product type added WITHOUT
    # changing the Product class. Billed every few months.

    PRODUCT_TYPE = "subscription"

    def __init__(self, product_id, name, price, stock, billing_months):
        super().__init__(product_id, name, price, stock)
        self.__billing_months = int(billing_months)

    def get_billing_months(self):
        return self.__billing_months

    def display_information(self):
        super().display_information()
        print("    Type: Subscription | Billed every " + str(self.__billing_months) + " month(s)")

    def get_fulfilment_info(self):
        return "This product is delivered as account access, renewed every " \
               + str(self.__billing_months) + " month(s)."

    def to_dict(self):
        data = super().to_dict()
        data["type"] = self.PRODUCT_TYPE
        data["billing_months"] = self.__billing_months
        return data

    @classmethod
    def from_dict(cls, data):
        return cls(data["id"], data["name"], data["price"], data["stock"], data["billing_months"])
