from abc import ABC, abstractmethod


class DiscountStrategy(ABC):
    # Strategy pattern: every discount provides the same apply() method.
    # Order only calls apply() and never needs to know which discount it is.

    @abstractmethod
    def apply(self, total: float) -> float:
        pass


class NoDiscount(DiscountStrategy):
    def apply(self, total: float) -> float:
        return total


class PercentageDiscount(DiscountStrategy):
    # PercentageDiscount(10) takes 10% off the total.

    def __init__(self, percentage: float):
        self.__percentage: float = percentage

    def apply(self, total: float) -> float:
        return total * (1 - self.__percentage / 100)


class BulkDiscount(DiscountStrategy):
    # BulkDiscount(200, 20) takes 20 off any total of 200 or more.

    def __init__(self, threshold: float, amount: float):
        self.__threshold: float = threshold
        self.__amount: float = amount

    def apply(self, total: float) -> float:
        if total >= self.__threshold:
            return total - self.__amount
        return total


class StudentDiscount(DiscountStrategy):
    # Added later as a new class - Order did not need to change (OCP).

    STUDENT_RATE: float = 0.05

    def apply(self, total: float) -> float:
        return total * (1 - self.STUDENT_RATE)
