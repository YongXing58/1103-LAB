import json
import os

from inventory import Inventory
from product_factory import ProductFactory
from supplier import Supplier


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

        # Products are created through the factory, never directly
        for item in data:
            try:
                supplier = Supplier.from_dict(item["supplier"])
                extra = item.get("weight", item.get("download_size", 0.0))
                product = ProductFactory.create(item["type"], item["id"], item["name"],
                                                item["price"], item["stock"], supplier, extra)
            except (ValueError, KeyError) as error:
                print("Skipping " + str(item.get("id")) + ": " + str(error))
                continue

            inventory.add_product(product)

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
