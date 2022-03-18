from dataclasses import dataclass
from enum import Enum


class PaymentMethod(Enum):
    CASH = 1
    CREDIT_CARD = 2


@dataclass(frozen=True)
class PaymentDetails:
    payment_method: PaymentMethod
    credit_card_number: str
    expires_month: int
    expires_year: int
    cardholder_name: str
