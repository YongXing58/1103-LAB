# ==========================================================
# INF1103 - Lab 2: Smart Inventory Auditor
# ==========================================================
# This program pretends to be a store manager's tool that
# checks ("audits") stock deliveries as they are typed in.

# ----------------------------------------------------------
# Requirement 1: Initialize the inventory to zero at the start
# ----------------------------------------------------------
total_inventory = 0        # running total of all accepted stock units
failed_entries = 0         # counts how many entries were rejected

# ----------------------------------------------------------
# Requirement 2: Run in a continuous loop until user types "quit"
# ----------------------------------------------------------
# A "while True" loop repeats forever until we hit a "break".
# We ask the user for input on every loop, and only stop when
# they type "quit".
while True:

    user_input = input("Enter stock quantity to add (or type 'quit' to stop): ")

    # Check if the user wants to stop the program
    if user_input == "quit":
        break   # this immediately exits the while loop

    # --------------------------------------------------------
    # Requirement 3 & 4: Accept integers only, reject invalid input
    # --------------------------------------------------------
    # .isdigit() returns True only if every character is a digit
    # (0-9). This means text like "ten" and negative numbers like
    # "-5" (because "-" is not a digit) will both fail this check.
    if not user_input.isdigit():
        print("Error: '" + user_input + "' is not a valid whole number. Entry rejected.")
        failed_entries = failed_entries + 1
        continue   # skip the rest of this loop, go ask for the next entry

    # If we reach this line, the input is safe to convert to an integer
    stock_quantity = int(user_input)

    # --------------------------------------------------------
    # Requirement 5: Enforce business rules - reject negative numbers
    # --------------------------------------------------------
    # Note: .isdigit() already blocks a typed "-5" above (since the
    # minus sign is not a digit), but we keep this explicit check
    # here as our business rule.
    if stock_quantity < 0:
        print("Error: Negative quantities are not allowed. Entry rejected.")
        failed_entries = failed_entries + 1
        continue

    # --------------------------------------------------------
    # Requirement 6: Manage state - keep a running total
    # --------------------------------------------------------
    else:
        total_inventory = total_inventory + stock_quantity
        print("Accepted. Current total inventory:", total_inventory)
