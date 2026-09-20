# ==========================================================
# INF1103 - Lab 3: Modular Auditor (refactored from Week 2)
# ==========================================================
# Same behaviour as auditor.py, but broken up into small,
# reusable functions instead of one big loop. Each function
# takes input as parameters and returns a value - it does not
# rely on variables from outside itself. This is what "pure"
# means in this week's requirements.


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
