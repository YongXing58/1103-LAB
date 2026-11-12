from order_line import OrderLine
from product import Product


class Order:
    # Responsibility: a customer order made up of order lines.
    # Composition: the Order creates and manages its own OrderLine
    # objects. Lines are never created elsewhere or moved between orders.

    def __init__(self, order_id: str):
        self.order_id: str = order_id
        self.order_lines: list[OrderLine] = []

    def add_order_line(self, product: Product, quantity: int) -> None:
        # The Order creates the OrderLine itself.
        order_line = OrderLine(product, quantity)
        self.order_lines.append(order_line)

    def remove_order_line(self, product_id: str) -> bool:
        # Removes the line for that product. The line is discarded with
        # the order; the Product is not affected.
        for order_line in self.order_lines:
            if order_line.product.get_product_id() == product_id:
                self.order_lines.remove(order_line)
                return True

        return False

    def calculate_total(self) -> float:
        # Asks each OrderLine for its subtotal.
        return sum(line.calculate_subtotal() for line in self.order_lines)

    def display_order(self) -> None:
        print("Order " + self.order_id)
        for order_line in self.order_lines:
            order_line.display_information()
        print("Total: $" + format(self.calculate_total(), ".2f"))
