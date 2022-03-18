from smtplib import SMTP
from typing import List

from cart import Cart, OrderItem
from services.inventory_system import InventorySystem, InsufficientInventoryError
from payment_details import PaymentDetails, PaymentMethod
from services.payment_gateway import PaymentGateway


class OrderError(Exception):
    pass


class NotificationService:
    def notify_customer_order_checked_out(self, cart: Cart):
        assert cart.customer_email

        sender_email = "shop@email.com"
        receiver_email = cart.customer_email
        message = f"Subject: Purchase Confirmation\nTotal Amount: {cart.total_amount:.2f}$"

        try:
            with SMTP("localhost") as smtp:
                smtp.sendmail(sender_email, receiver_email, message)
        except:
            print("Error! Sending email failed!")


class ReservationService:
    def __init__(self, inventory_system=None):
        self._inventory_system = inventory_system if inventory_system else InventorySystem()

    def reserve_inventory(self, items: List[OrderItem]):
        try:
            for item in items:
                self._inventory_system.reserve(item.sku, item.quantity)
        except InsufficientInventoryError:
            raise OrderError(f"Insufficient inventory for item: {item.sku}")
        except Exception:
            raise OrderError("Problem with reserving inventory")


class PaymentService:
    def process_credit_card(self, payment_details: PaymentDetails, amount: float):
        with PaymentGateway() as payment_gateway:
            payment_gateway.credentials = "account credentials"
            payment_gateway.card_number = payment_details.credit_card_number
            payment_gateway.expires_month = payment_details.expires_month
            payment_gateway.expires_year = payment_details.expires_month
            payment_gateway.name_on_card = payment_details.cardholder_name
            payment_gateway.amount_to_charge = amount

            payment_gateway.charge()


class Order:
    # def __init__(self,
    #              notification_service=None,
    #              reservation_service=None,
    #              payment_service=None):
    #     """Dependency Injection"""
    #     self._notification_service = notification_service if notification_service else NotificationService()
    #     self._reservation_service = reservation_service if reservation_service else ReservationService()
    #     self._payment_service = payment_service if payment_service else PaymentService()

    def __init__(self):
        """
        No dependency injection
        """
        self._notification_service = NotificationService()
        self._reservation_service = ReservationService()
        self._payment_service = PaymentService()

    def checkout(self, cart: Cart, payment_details: PaymentDetails, notify_customer: bool):
        if payment_details.payment_method == PaymentMethod.CREDIT_CARD:
            self._payment_service.process_credit_card(payment_details, cart.total_amount)

        self._reservation_service.reserve_inventory(cart.items)

        if notify_customer:
            self._notification_service.notify_customer_order_checked_out(cart)

    def reserve_inventory(self, cart: Cart):
        try:
            inventory_system = InventorySystem()

            for item in cart.items:
                inventory_system.reserve(item.sku, item.quantity)
        except InsufficientInventoryError:
            raise OrderError(f"Insufficient inventory for item: {item.sku}")
        except Exception:
            raise OrderError("Problem with reserving inventory")
