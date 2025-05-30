# service/order_service.py

from model.order import Order
from model.errors import (
    PaymentDeclinedError,
    MissingPaymentMethodError,
    MissingAddressError,
)


class OrderService:
    @staticmethod
    def place_order(
        items: list, payment_method, address: str, note: str = None
    ) -> Order:
        """
        Complete an order:
          1) Validate that a payment method and address exist.
          2) Calculate total.
          3) Process payment via the method's provider.
          4) On success, create & confirm an Order.
        """

        # 1) Basic validation
        if payment_method is None:
            raise MissingPaymentMethodError("You must select a payment method.")
        if not address or not address.strip():
            raise MissingAddressError("A delivery address is required.")

        # 2) Total amount
        total = sum(item.price for item in items)

        # 3) Charge
        provider = getattr(payment_method, "provider", None)
        if provider is None:
            # assume payment_method itself can process
            success = payment_method.processTransaction(payment_method, total)
        else:
            success = provider.processTransaction(payment_method, total)

        if not success:
            raise PaymentDeclinedError("Payment was declined by the provider.")

        # 4) Create and confirm order
        order = Order(items, total, address, note)
        order.confirm()
        return order
