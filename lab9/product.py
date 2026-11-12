from abc import ABC, abstractmethod

from supplier import Supplier


class Product(ABC):
    # Responsibility: represent and manage a single product.
    # Abstract: every product must be a specific type (physical,
    # digital, ...), so Product itself cannot be instantiated.

    def __init__(self, product_id: str, name: str, price: float,
                 stock_quantity: int, supplier: Supplier):
        # Validation: the Product protects its own rules.
        if float(price) <= 0:
            raise ValueError("Price must be greater than zero.")

        self.__product_id: str = product_id
        self.__name: str = name
        self.__price: float = float(price)
        self.__stock: int = 0
        self.update_stock(stock_quantity)
        # Association: the product keeps a reference to its supplier,
        # but does not own it. The supplier exists independently.
        self.supplier: Supplier = supplier

    # Read-only access to the private attributes.
    # There are no setters, so outside code cannot change them directly.
    def get_product_id(self) -> str:
        return self.__product_id

    def get_name(self) -> str:
        return self.__name

    def get_price(self) -> float:
        return self.__price

    def get_stock(self) -> int:
        return self.__stock

    def update_stock(self, quantity: int) -> None:
        # The only way to change stock. The Product decides what
        # counts as valid, so its stock can never become invalid.
        # Subclasses keep this rule (LSP) - they do not skip or change it.
        if not isinstance(quantity, int) or quantity < 0:
            raise ValueError("Stock quantity cannot be negative.")

        self.__stock = quantity

    def display_information(self) -> None:
        # Shows the common information. Subclasses override this,
        # call it with super() and then add their own details.
        print("ID: " + self.__product_id
              + " | Name: " + self.__name
              + " | Price: $" + format(self.__price, ".2f")
              + " | Stock: " + str(self.__stock))

    def to_dict(self) -> dict:
        # The common data as a dictionary (used for saving to JSON).
        # Subclasses override this, call it with super() and add
        # their type identifier and extra attributes.
        return {
            "id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
            "supplier": self.supplier.to_dict()
        }

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        # Each product type must explain how it reaches the customer.
        pass
