from discount_strategy import DiscountStrategy, NoDiscount
from order_line import OrderLine
from product import Product


class Order:
    # Responsibility: a customer order made up of order lines.
    # Composition: the Order creates and manages its own OrderLine objects.
    # Association: the Order uses a DiscountStrategy but does not own it,
    # so the same strategy object can be shared by several orders.

    def __init__(self, order_id: str, discount: DiscountStrategy | None = None):
        self.order_id: str = order_id
        self.order_lines: list[OrderLine] = []
        # No checking of discount types here - just hold a strategy.
        self.discount: DiscountStrategy = discount if discount is not None else NoDiscount()

    def set_discount(self, discount: DiscountStrategy) -> None:
        self.discount = discount

    def add_order_line(self, product: Product, quantity: int) -> None:
        # The Order creates the OrderLine itself.
        order_line = OrderLine(product, quantity)
        self.order_lines.append(order_line)

    def remove_order_line(self, product_id: str) -> bool:
        for order_line in self.order_lines:
            if order_line.product.get_product_id() == product_id:
                self.order_lines.remove(order_line)
                return True

        return False

    def calculate_total(self) -> float:
        total = sum(line.calculate_subtotal() for line in self.order_lines)
        return self.discount.apply(total)

    def display_order(self) -> None:
        print("Order " + self.order_id)
        for order_line in self.order_lines:
            order_line.display_information()
        print("Total: $" + format(self.calculate_total(), ".2f"))
