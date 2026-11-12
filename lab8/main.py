from can_be_shipped import CanBeShipped
from inventory import Inventory
from inventory_file import InventoryFile
from product_types import PRODUCT_TYPES
from supplier import Supplier

INVENTORY_FILE = "inventory.json"


def get_number(prompt: str, number_type=float):
    # Keeps asking until the user enters a valid non-negative number.
    while True:
        user_input = input(prompt)
        try:
            number = number_type(user_input)
        except ValueError:
            print("Error: '" + user_input + "' is not a valid number.")
            continue

        if number < 0:
            print("Error: value cannot be negative.")
            continue

        return number


def get_quantity(prompt: str) -> int:
    # Keeps asking until the user enters a valid whole number.
    while True:
        user_input = input(prompt)

        # .isdigit() also rejects negative numbers and decimals
        if user_input.isdigit():
            return int(user_input)

        print("Error: '" + user_input + "' is not a valid whole number.")


def choose_product_type() -> str:
    # Lists every registered product type and returns the chosen type id.
    type_ids = list(PRODUCT_TYPES.keys())

    print("\nProduct Type")
    for i in range(len(type_ids)):
        print(str(i + 1) + ". " + PRODUCT_TYPES[type_ids[i]][0])

    while True:
        choice = input("Choose type: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(type_ids):
            return type_ids[int(choice) - 1]

        print("Error: please enter a number from 1 to " + str(len(type_ids)) + ".")


def get_supplier(inventory: Inventory) -> Supplier:
    # Reuses an existing Supplier object if the ID is already known,
    # otherwise asks for the details and creates a new one.
    supplier_id = input("Supplier ID: ").strip().upper()

    for product in inventory.get_all_products():
        if product.supplier.supplier_id == supplier_id:
            return product.supplier

    name = input("Supplier Name: ").strip()
    email = input("Supplier Email: ").strip()
    return Supplier(supplier_id, name, email)


def show_menu() -> None:
    print("\n----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("----------------------------")


def menu_add(inventory: Inventory) -> None:
    print("\nAdd New Product")
    product_type = choose_product_type()
    label, product_class, extra_prompt = PRODUCT_TYPES[product_type]

    product_id = input("Product ID: ").strip().upper()

    if product_id == "":
        print("Error: Product ID cannot be empty.")
        return

    if inventory.find_product(product_id) is not None:
        print("Error: Product ID " + product_id + " already exists.")
        return

    name = input("Product Name: ").strip()
    price = get_number("Price: ")
    stock = get_quantity("Stock Quantity: ")
    supplier = get_supplier(inventory)
    extra = get_number(extra_prompt)

    product = product_class(product_id, name, price, stock, supplier, extra)
    inventory.add_product(product)
    print("\n" + label + " added successfully!")


def menu_update(inventory: Inventory) -> None:
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ").strip().upper()
    product = inventory.find_product(product_id)

    if product is None:
        print("\nProduct not found.")
        return

    print("\nProduct Found:")
    print("Name: " + product.get_name())
    print("Current Stock: " + str(product.get_stock()))

    new_stock = get_quantity("\nNew Stock Quantity: ")
    if product.update_stock(new_stock):
        print("\nStock updated successfully!")
    else:
        print("\nError: stock could not be updated.")


def menu_search(inventory: Inventory) -> None:
    print("\nSearch Product")
    product_id = input("Enter Product ID: ").strip().upper()
    product = inventory.find_product(product_id)

    if product is None:
        print("\nProduct not found.")
        return

    print("\nProduct Found")
    print("-" * 60)
    product.display_information()
    product.supplier.display_information()
    print("Fulfilment: " + product.get_fulfilment_info())

    # Only products that sign the CanBeShipped contract have a shipping cost
    if isinstance(product, CanBeShipped):
        print("Shipping Cost: $" + format(product.calculate_shipping_cost(), ".2f"))
    print("-" * 60)


# ----------------------------------------------------------
# Main program
# ----------------------------------------------------------

if __name__ == "__main__":
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)
    print()

    inventory_file = InventoryFile(INVENTORY_FILE)
    inventory = inventory_file.load()

    while True:
        show_menu()
        option = input("\nEnter option: ").strip()

        if option == "1":
            inventory.display_all_products()
        elif option == "2":
            menu_add(inventory)
        elif option == "3":
            menu_update(inventory)
        elif option == "4":
            menu_search(inventory)
        elif option == "5":
            print("\nSaving inventory...")
            inventory_file.save(inventory)
            print("Inventory saved successfully to " + INVENTORY_FILE + ".")
        elif option == "6":
            print("\nSaving inventory before exit...")
            inventory_file.save(inventory)
            print("Inventory saved successfully.")
            print("\nThank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid option. Please enter a number from 1 to 6.")
