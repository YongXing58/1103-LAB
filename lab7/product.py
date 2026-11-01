from abc import ABC, abstractmethod


class Product(ABC):
    # Responsibility: represent and manage a single product.
    # Abstract: every product must be a specific type (physical,
    # digital, ...), so Product itself cannot be instantiated.

    def __init__(self, product_id, name, price, stock):
        self.__product_id = product_id
        self.__name = name
        self.__price = float(price)
        self.__stock = 0
        self.update_stock(stock)

    # Read-only access to the private attributes.
    # There are no setters, so outside code cannot change them directly.
    def get_product_id(self):
        return self.__product_id

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def get_stock(self):
        return self.__stock

    def update_stock(self, quantity):
        # The only way to change stock. The Product decides what
        # counts as valid, so its stock can never become invalid.
        # Returns True if updated, False if the quantity was rejected.
        if not isinstance(quantity, int) or quantity < 0:
            return False

        self.__stock = quantity
        return True

    def display_information(self):
        # Shows the common information. Subclasses override this,
        # call it with super() and then add their own details.
        print("ID: " + self.__product_id
              + " | Name: " + self.__name
              + " | Price: $" + format(self.__price, ".2f")
              + " | Stock: " + str(self.__stock))

    def to_dict(self):
        # The common data as a dictionary (used for saving to JSON).
        # Subclasses override this, call it with super() and add
        # their type identifier and extra attributes.
        return {
            "id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock
        }

    @abstractmethod
    def get_fulfilment_info(self):
        # Each product type must explain how it reaches the customer.
        pass
