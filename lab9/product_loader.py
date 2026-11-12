import csv

from inventory import Inventory
from product_factory import ProductFactory
from supplier import Supplier


def load_products(path: str, inventory: Inventory, supplier: Supplier) -> None:
    # Reads products from a CSV file and adds them to the inventory.
    loaded = 0
    try:
        file = open(path, newline="")
    except FileNotFoundError:
        print(f"Products file not found: {path}")
    else:
        with file:
            reader = csv.reader(file)
            next(reader, None)  # skip the header row

            for row in reader:
                try:
                    product_type, product_id, name, price, stock_quantity = row
                    product = ProductFactory.create(product_type, product_id, name,
                                                    float(price), int(stock_quantity), supplier)
                except ValueError as error:
                    print(f"Skipping row {reader.line_num}: {error}")
                    continue

                if inventory.add_product(product):
                    loaded += 1
                else:
                    print(f"Skipping row {reader.line_num}: product ID {product_id} already exists.")

        print(f"{loaded} products loaded.")
    finally:
        print("Load attempt finished.")
