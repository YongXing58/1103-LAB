class Inventory:
    # Responsibility: manage a collection of Product objects.

    def __init__(self):
        self.__products = []

    def add_product(self, product):
        # Returns True if added, False if the product ID already exists.
        if self.search_product(product.get_product_id()) is not None:
            return False

        self.__products.append(product)
        return True

    def search_product(self, product_id):
        # Returns the matching Product object, or None if not found.
        for product in self.__products:
            if product.get_product_id() == product_id:
                return product

        return None

    def get_all_products(self):
        # Returns a copy so outside code cannot change the internal list.
        return list(self.__products)

    def display_all(self):
        print("\nCurrent Inventory")
        print("-" * 48)

        if len(self.__products) == 0:
            print("No products in inventory.")

        for product in self.__products:
            product.display_information()

        print("-" * 48)
