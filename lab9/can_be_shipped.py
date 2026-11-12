from abc import ABC, abstractmethod


class CanBeShipped(ABC):
    # Interface: a contract for anything that can be shipped.
    # It only says WHAT must be provided, not HOW, so it holds
    # no attributes or shipping details of its own.

    @abstractmethod
    def calculate_shipping_cost(self):
        # Implementing classes must return the shipping cost as a float.
        pass
