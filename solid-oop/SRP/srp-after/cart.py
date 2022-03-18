from dataclasses import dataclass


@dataclass(frozen=True)
class OrderItem:
    sku: str
    quantity: int


@dataclass(frozen=True)
class Cart:
    total_amount: float
    items: list[OrderItem]
    customer_email: str
