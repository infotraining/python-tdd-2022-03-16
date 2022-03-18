from unittest.mock import patch, ANY

from order import Order
from cart import OrderItem, Cart
from payment_details import PaymentDetails, PaymentMethod

from callee import String, StartsWith


def test_when_checkout_order_purchase_confirmation_email_is_send():
    cart = Cart(total_amount=99.99, items=[OrderItem("AA11BB", 1)], customer_email="customer@email.com")
    payment_details = PaymentDetails(payment_method=PaymentMethod.CREDIT_CARD,
                                     credit_card_number="11112222333344",
                                     expires_month=1,
                                     expires_year=2025,
                                     cardholder_name="John Smith")

    order = Order()

    with patch('order.SMTP', autospec=True) as mock_smtp, \
            patch('order.InventorySystem', autospec=True) as mock_inventory, \
            patch('order.PaymentGateway', autospec=True) as mock_payment_gateway:
        order.checkout(cart, payment_details, True)

        context = mock_smtp.return_value.__enter__.return_value
        context.sendmail.assert_called_with("shop@email.com",
                                            "customer@email.com",
                                            String() & StartsWith("Subject: Purchase Confirmation"))


def test_when_checkout_items_are_reserved_in_inventory():
    cart = Cart(total_amount=99.99, items=[OrderItem("AA11BB", 1)], customer_email="customer@email.com")
    payment_details = PaymentDetails(payment_method=PaymentMethod.CREDIT_CARD,
                                     credit_card_number="11112222333344",
                                     expires_month=1,
                                     expires_year=2025,
                                     cardholder_name="John Smith")

    order = Order()

    with patch('order.SMTP', autospec=True) as mock_smtp, \
            patch('order.InventorySystem', autospec=True) as mock_inventory, \
            patch('order.PaymentGateway', autospec=True) as mock_payment_gateway:
        order.checkout(cart, payment_details, True)

        mock_inventory.return_value.reserve.assert_called_with("AA11BB", 1)


def test_when_checkout_card_is_charged_with_total_amount():
    cart = Cart(total_amount=99.99, items=[OrderItem("AA11BB", 1)], customer_email="customer@email.com")
    payment_details = PaymentDetails(payment_method=PaymentMethod.CREDIT_CARD,
                                     credit_card_number="11112222333344",
                                     expires_month=1,
                                     expires_year=2025,
                                     cardholder_name="John Smith")

    order = Order()

    with patch('order.SMTP', autospec=True) as mock_smtp, \
            patch('order.InventorySystem', autospec=True) as mock_inventory, \
            patch('order.PaymentGateway', autospec=True) as mock_payment_gateway:
        order.checkout(cart, payment_details, True)

        assert mock_payment_gateway.return_value.__enter__.return_value.amount_to_charge == 99.99
        mock_payment_gateway.return_value.__enter__.assert_called()
