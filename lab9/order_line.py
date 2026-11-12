from product import Product


class OrderLine:
    # Responsibility: one product and the quantity ordered.
    # Composition: an OrderLine belongs to exactly one Order, which
    # creates it. It refers to a Product but does not own it.

    def __init__(self, product: Product, quantity: int):
        # The OrderLine protects its own quantity rule.
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")

        self.product: Product = product
        self.quantity: int = quantity

    def calculate_subtotal(self) -> float:
        return self.product.get_price() * self.quantity

    def display_information(self) -> None:
        print(self.product.get_name() + " x " + str(self.quantity)
              + " = $" + format(self.calculate_subtotal(), ".2f"))
