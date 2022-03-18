from dataclasses import dataclass, field


@dataclass
class PaymentGateway:
    credentials: str = field(default="not-set")
    card_number: str = field(default="not-set")
    expires_month: int = field(default=0)
    expires_year: int = field(default=0)
    name_on_card: str = field(default="not-set")
    amount_to_charge: float = field(default=0.0)

    def charge(self):
        print(f"Card {self.card_number} charged {self.amount_to_charge}$")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
