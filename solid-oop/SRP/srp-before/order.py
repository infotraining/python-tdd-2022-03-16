from smtplib import SMTP

from cart import Cart
from services.inventory_system import InventorySystem, InsufficientInventoryError
from payment_details import PaymentDetails, PaymentMethod
from services.payment_gateway import PaymentGateway


class OrderError(Exception):
    pass


class Order:
    def checkout(self, cart: Cart, payment_details: PaymentDetails, notify_customer: bool):
        if payment_details.payment_method == PaymentMethod.CREDIT_CARD:
            self.charge_card(payment_details, cart)

        self.reserve_inventory(cart)

        if notify_customer:
            self.notify_customer(cart)

    def notify_customer(self, cart: Cart):
        if cart.customer_email:
            sender_email = "shop@email.com"
            receiver_email = cart.customer_email
            message = f"Subject: Purchase Confirmation\nTotal Amount: {cart.total_amount:.2f}$"

            try:
                with SMTP("localhost") as smtp:
                    smtp.sendmail(sender_email, receiver_email, message)
            except:
                print("Error! Sending email failed!")

    def reserve_inventory(self, cart: Cart):
        try:
            inventory_system = InventorySystem()

            for item in cart.items:
                inventory_system.reserve(item.sku, item.quantity)
        except InsufficientInventoryError:
            raise OrderError(f"Insufficient inventory for item: {item.sku}")
        except:
            raise OrderError("Problem with reserving inventory")

    def charge_card(self, payment_details: PaymentDetails, cart: Cart):
        with PaymentGateway() as payment_gateway:
            payment_gateway.credentials = "account credentials"
            payment_gateway.card_number = payment_details.credit_card_number
            payment_gateway.expires_month = payment_details.expires_month
            payment_gateway.expires_year = payment_details.expires_month
            payment_gateway.name_on_card = payment_details.cardholder_name
            payment_gateway.amount_to_charge = cart.total_amount

            payment_gateway.charge()
