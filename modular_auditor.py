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
