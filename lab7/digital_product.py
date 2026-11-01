from product import Product


class DigitalProduct(Product):
    # Responsibility: a product that is delivered by download.
    # It does NOT implement CanBeShipped, because it is never shipped.

    PRODUCT_TYPE = "digital"

    def __init__(self, product_id, name, price, stock, download_size):
        # Reuse the Product constructor for the common attributes.
        super().__init__(product_id, name, price, stock)
        self.__download_size = float(download_size)

    def get_download_size(self):
        return self.__download_size

    def display_information(self):
        # Overrides Product.display_information(): the parent prints
        # the common details, this class adds only what is unique to it.
        super().display_information()
        print("    Type: Digital | Download Size: " + format(self.__download_size, ".2f") + " MB")

    def get_fulfilment_info(self):
        return "This product is delivered digitally via a download link."

    def to_dict(self):
        data = super().to_dict()
        data["type"] = self.PRODUCT_TYPE
        data["download_size"] = self.__download_size
        return data

    @classmethod
    def from_dict(cls, data):
        return cls(data["id"], data["name"], data["price"], data["stock"], data["download_size"])
