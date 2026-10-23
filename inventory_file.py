import json
import os

from inventory import Inventory
from product import Product


class InventoryFile:
    # Responsibility: load and save an Inventory to a JSON file.

    def __init__(self, file_name):
        self.__file_name = file_name

    def get_file_name(self):
        return self.__file_name

    def load(self):
        # Returns an Inventory built from the JSON file,
        # or an empty Inventory if the file does not exist yet.
        inventory = Inventory()

        if not os.path.exists(self.__file_name):
            print(self.__file_name + " not found. Starting with an empty inventory.")
            return inventory

        print(self.__file_name + " found.")
        with open(self.__file_name, "r") as f:
            data = json.load(f)

        # Turn each dictionary from the file back into a Product object
        for item in data:
            product = Product(item["id"], item["name"], item["price"], item["stock"])
            inventory.add_product(product)

        print("Inventory loaded successfully.")
        return inventory

    def save(self, inventory):
        # JSON can't store objects, so each Product is turned into
        # a dictionary using its public getters before writing.
        data = []
        for product in inventory.get_all_products():
            data.append({
                "id": product.get_product_id(),
                "name": product.get_name(),
                "price": product.get_price(),
                "stock": product.get_stock()
            })

        with open(self.__file_name, "w") as f:
            json.dump(data, f, indent=4)
