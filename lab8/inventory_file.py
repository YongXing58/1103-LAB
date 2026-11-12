import json
import os

from inventory import Inventory
from product_types import get_product_class


class InventoryFile:
    # Responsibility: load and save an Inventory to a JSON file.

    def __init__(self, file_name: str):
        self.__file_name: str = file_name

    def get_file_name(self) -> str:
        return self.__file_name

    def load(self) -> Inventory:
        # Returns an Inventory built from the JSON file,
        # or an empty Inventory if the file does not exist yet.
        inventory = Inventory()

        if not os.path.exists(self.__file_name):
            print(self.__file_name + " not found. Starting with an empty inventory.")
            return inventory

        print(self.__file_name + " found.")
        with open(self.__file_name, "r") as f:
            data = json.load(f)

        # Use each item's "type" identifier to rebuild the right subclass
        for item in data:
            product_class = get_product_class(item.get("type"))
            if product_class is None:
                print("Skipping " + str(item.get("id")) + ": unknown product type '"
                      + str(item.get("type")) + "'.")
                continue

            inventory.add_product(product_class.from_dict(item))

        print("Inventory loaded successfully.")
        return inventory

    def save(self, inventory: Inventory) -> None:
        # JSON can't store objects, so each product turns itself into a
        # dictionary (including its type, supplier and extra attributes) first.
        data = []
        for product in inventory.get_all_products():
            data.append(product.to_dict())

        with open(self.__file_name, "w") as f:
            json.dump(data, f, indent=4)
