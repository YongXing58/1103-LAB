from product import Product


class Inventory:
    # Responsibility: manage a collection of Product objects.
    # Aggregation: the inventory holds references to products, but does
    # not own them - a product can be removed and still be used, or
    # added to another inventory.
    # It works with any Product subclass and never needs to know
    # which type a product is - it just calls the product's methods.

    def __init__(self):
        self.__products: list[Product] = []

    def add_product(self, product: Product) -> bool:
        # Returns True if added, False if the product ID already exists.
        if self.find_product(product.get_product_id()) is not None:
            return False

        self.__products.append(product)
        return True

    def remove_product(self, product_id: str) -> bool:
        # Removes only the reference. The Product itself is not destroyed.
        # Returns True if removed, False if the ID was not found.
        product = self.find_product(product_id)
        if product is None:
            return False

        self.__products.remove(product)
        return True

    def find_product(self, product_id: str) -> Product | None:
        # Returns the matching Product object, or None if not found.
        for product in self.__products:
            if product.get_product_id() == product_id:
                return product

        return None

    def get_all_products(self) -> list[Product]:
        # Returns a copy so outside code cannot change the internal list.
        return list(self.__products)

    def display_all_products(self) -> None:
        print("\nCurrent Inventory")
        print("-" * 60)

        if len(self.__products) == 0:
            print("No products in inventory.")

        for product in self.__products:
            product.display_information()

        print("-" * 60)
