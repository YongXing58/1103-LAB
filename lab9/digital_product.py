from product import Product
from supplier import Supplier


class DigitalProduct(Product):
    # Responsibility: a product that is delivered by download.
    # It does NOT implement CanBeShipped, because it is never shipped.

    PRODUCT_TYPE: str = "digital"

    def __init__(self, product_id: str, name: str, price: float,
                 stock_quantity: int, supplier: Supplier, download_size: float):
        # Reuse the Product constructor for the common attributes.
        super().__init__(product_id, name, price, stock_quantity, supplier)
        self.__download_size: float = float(download_size)

    def get_download_size(self) -> float:
        return self.__download_size

    def display_information(self) -> None:
        # Overrides Product.display_information(): the parent prints
        # the common details, this class adds only what is unique to it.
        super().display_information()
        print("    Type: Digital | Download Size: " + format(self.__download_size, ".2f") + " MB")

    def get_fulfilment_info(self) -> str:
        return "This product is delivered digitally via a download link."

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["type"] = self.PRODUCT_TYPE
        data["download_size"] = self.__download_size
        return data
