from inventory_file import InventoryFile
from product import Product

INVENTORY_FILE = "inventory.json"


def get_price(prompt):
    # Keeps asking until the user enters a valid non-negative number.
    while True:
        user_input = input(prompt)
        try:
            price = float(user_input)
        except ValueError:
            print("Error: '" + user_input + "' is not a valid price.")
            continue

        if price < 0:
            print("Error: price cannot be negative.")
            continue

        return price


def get_quantity(prompt):
    # Keeps asking until the user enters a valid whole number.
    while True:
        user_input = input(prompt)

        # .isdigit() also rejects negative numbers and decimals
        if user_input.isdigit():
            return int(user_input)

        print("Error: '" + user_input + "' is not a valid whole number.")


def show_menu():
    print("\n----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("----------------------------")


def menu_add(inventory):
    print("\nAdd New Product")
    product_id = input("Product ID: ").strip().upper()

    if product_id == "":
        print("Error: Product ID cannot be empty.")
        return

    if inventory.search_product(product_id) is not None:
        print("Error: Product ID " + product_id + " already exists.")
        return

    name = input("Product Name: ").strip()
    price = get_price("Price: ")
    stock = get_quantity("Stock Quantity: ")

    product = Product(product_id, name, price, stock)
    inventory.add_product(product)
    print("\nProduct added successfully!")


def menu_update(inventory):
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ").strip().upper()
    product = inventory.search_product(product_id)

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


def menu_search(inventory):
    print("\nSearch Product")
    product_id = input("Enter Product ID: ").strip().upper()
    product = inventory.search_product(product_id)

    if product is None:
        print("\nProduct not found.")
        return

    print("\nProduct Found")
    print("-" * 48)
    product.display_information()
    print("-" * 48)


# ----------------------------------------------------------
# Main program
# ----------------------------------------------------------

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
        inventory.display_all()
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
