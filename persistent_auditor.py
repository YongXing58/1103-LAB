import os


def load_inventory():
    """
    Requirement 1 & 4: load_inventory()
    Takes:   nothing.
    Returns: a tuple (total, history) -
             total   = the saved running total (int)
             history = the saved list of past transaction amounts

    Why check os.path.exists() first: opening a file that doesn't
    exist yet (e.g. the very first time the program ever runs)
    would crash the program with a FileNotFoundError. The lab
    requires we handle that case quietly instead - so we check
    BEFORE trying to open the file, and simply return "empty"
    starting values (0 and []) if it's not there yet.
    """
    if not os.path.exists("inventory.txt"):
        return 0, []

    with open("inventory.txt", "r") as f:
        lines = f.readlines()

    # Why lines[0]: we chose a simple file format where the first
    # line holds the total, so we always read that line and convert
    # it back from text to an integer.
    total = int(lines[0].strip())

    # Why the length check: if the history line is missing or blank
    # (e.g. every entry so far was invalid/rejected), splitting an
    # empty string on "," would incorrectly produce [''] instead of
    # [] - so we only split when there is actually something there.
    if len(lines) > 1 and lines[1].strip() != "":
        history = [int(value) for value in lines[1].strip().split(",")]
    else:
        history = []

    return total, history


def get_valid_input():
    """
    Requirement function 1: get_valid_input()
    Takes:   nothing.
    Returns: a valid non-negative integer, the string "quit",
             or None if the entry was invalid.
    """
    user_input = input("Enter stock quantity to add (or type 'quit' to stop): ")

    if user_input == "quit":
        return "quit"

    # .isdigit() also blocks negative numbers, since "-" is not a digit,
    # so a separate negative-number check is not needed here.
    if not user_input.isdigit():
        print("Error: '" + user_input + "' is not a valid whole number. Entry rejected.")
        return None

    stock_quantity = int(user_input)
    return stock_quantity


def process_delivery(current_total, new_value):
    """
    Requirement function 2: process_delivery(current_total, new_value)
    Takes:   the current running total, and the new delivery amount.
    Returns: the new running total (current_total + new_value).

    This function only calculates and returns a value - it does not
    print anything and does not decide whether to stop the loop.
    """
    new_total = current_total + new_value
    return new_total


def calculate_tax(amount):
    """
    Requirement function 3: calculate_tax(amount)
    Takes:   the amount of one delivery.
    Returns: the tax for that delivery (10% of the amount).
    """
    tax_rate = 0.1
    return amount * tax_rate


def generate_report(total_units, failed_attempts):
    """
    Requirement function 4: generate_report(total_units, failed_attempts)
    Takes:   the total inventory processed and the number of failed entries.
    Returns: nothing - this function's only job is to print the summary.
    """
    print("\n----- Inventory Audit Report -----")
    print("Total Deliveries Processed:", total_units)
    print("Number of Failed/Rejected Entries:", failed_attempts)


# ----------------------------------------------------------
# Main program: ties the functions above together
# ----------------------------------------------------------

# Requirement 1: Load whatever was saved last time (or start empty)
# Why we replaced "total_inventory = 0" with a call to load_inventory():
# the whole point of this week's lab is that the starting value should
# come from disk, not always reset to zero, so the data survives after
# the container stops and restarts.
total_inventory, history = load_inventory()
failed_entries = 0         # count of rejected entries (this one is NOT
                            # persisted - the lab only asks us to save the
                            # total and the transaction history)

# Requirement 2: Run in a continuous loop until the user types "quit"
while True:

    stock_quantity = get_valid_input()

    if stock_quantity == "quit":
        break

    if stock_quantity is None:
        # get_valid_input() already printed the error message for us
        failed_entries = failed_entries + 1
        continue

    # Requirement 3: valid value - update total and calculate tax
    total_inventory = process_delivery(total_inventory, stock_quantity)
    tax = calculate_tax(stock_quantity)

    # Requirement 2: History Tracking - record this valid transaction.
    # Why here specifically: this is the exact point in the loop where
    # we already know stock_quantity passed validation (get_valid_input()
    # rejected it earlier and used continue if it hadn't), so every value
    # that reaches this line is guaranteed to be one we want to remember.
    history.append(stock_quantity)

    print("Accepted. Delivery tax:", tax, "| Current total inventory:", total_inventory)

    if total_inventory > 500:
        print("OVERSTOCK ALERT: Inventory has exceeded 500 units! Stopping program.")
        break
    elif total_inventory == 500:
        print("Notice: Inventory has reached exactly 500 units.")

# Requirement 4: Reporting
generate_report(total_inventory, failed_entries)
