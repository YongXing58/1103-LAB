import json
import os

INVENTORY_FILE = "inventory.json"


def load_inventory():
    # Returns the list of products saved in inventory.json,
    # or an empty list if the file does not exist yet.
    if not os.path.exists(INVENTORY_FILE):
        print(INVENTORY_FILE + " not found. Starting with an empty inventory.")
        return []

    print(INVENTORY_FILE + " found.")
    with open(INVENTORY_FILE, "r") as f:
        inventory = json.load(f)

    print("Inventory loaded successfully.")
    return inventory


def save_inventory(inventory):
    # Writes the whole inventory list to inventory.json.
    # indent=4 keeps the file readable if you open it in an editor.
    with open(INVENTORY_FILE, "w") as f:
        json.dump(inventory, f, indent=4)


def add_product(inventory, product):
    # Takes the inventory list and a new product dictionary.
    # Returns True if added, False if the product ID already exists.
    if search_product(inventory, product["id"]) is not None:
        return False

    inventory.append(product)
    return True


def update_stock(inventory, product_id, new_stock):
    # Returns True if the product was found and updated, False otherwise.
    product = search_product(inventory, product_id)

    if product is None:
        return False

    product["stock"] = new_stock
    return True


def search_product(inventory, product_id):
    # Returns the matching product dictionary, or None if not found.
    for product in inventory:
        if product["id"] == product_id:
            return product

    return None


def display_all(inventory):
    print("\nCurrent Inventory")
    print("-" * 48)

    if len(inventory) == 0:
        print("No products in inventory.")

    for product in inventory:
        print("ID: " + product["id"]
              + " | Name: " + product["name"]
              + " | Price: $" + format(product["price"], ".2f")
              + " | Stock: " + str(product["stock"]))

    print("-" * 48)


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

    if search_product(inventory, product_id) is not None:
        print("Error: Product ID " + product_id + " already exists.")
        return

    name = input("Product Name: ").strip()
    price = get_price("Price: ")
    stock = get_quantity("Stock Quantity: ")

    product = {"id": product_id, "name": name, "price": price, "stock": stock}
    add_product(inventory, product)
    print("\nProduct added successfully!")


def menu_update(inventory):
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ").strip().upper()
    product = search_product(inventory, product_id)

    if product is None:
        print("\nProduct not found.")
        return

    print("\nProduct Found:")
    print("Name: " + product["name"])
    print("Current Stock: " + str(product["stock"]))

    new_stock = get_quantity("\nNew Stock Quantity: ")
    update_stock(inventory, product_id, new_stock)
    print("\nStock updated successfully!")


def menu_search(inventory):
    print("\nSearch Product")
    product_id = input("Enter Product ID: ").strip().upper()
    product = search_product(inventory, product_id)

    if product is None:
        print("\nProduct not found.")
        return

    print("\nProduct Found")
    print("-" * 48)
    print("ID: " + product["id"])
    print("Name: " + product["name"])
    print("Price: $" + format(product["price"], ".2f"))
    print("Stock: " + str(product["stock"]))
    print("-" * 48)


# ----------------------------------------------------------
# Main program
# ----------------------------------------------------------

print("=" * 40)
print("INVENTORY MANAGEMENT SYSTEM")
print("=" * 40)
print()

# Each product is a dictionary; the inventory is a list of them
inventory = load_inventory()

while True:
    show_menu()
    option = input("\nEnter option: ").strip()

    if option == "1":
        display_all(inventory)
    elif option == "2":
        menu_add(inventory)
    elif option == "3":
        menu_update(inventory)
    elif option == "4":
        menu_search(inventory)
    elif option == "5":
        print("\nSaving inventory...")
        save_inventory(inventory)
        print("Inventory saved successfully to " + INVENTORY_FILE + ".")
    elif option == "6":
        print("\nSaving inventory before exit...")
        save_inventory(inventory)
        print("Inventory saved successfully.")
        print("\nThank you for using Inventory Management System.")
        print("Program terminated.")
        break
    else:
        print("Invalid option. Please enter a number from 1 to 6.")
