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
