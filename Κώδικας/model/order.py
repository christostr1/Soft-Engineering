# model/order.py

import uuid
from datetime import datetime


class Order:
    """
    Represents a customer order.
    """

    def __init__(
        self,
        items: list,
        total_amount: float,
        delivery_address: str,
        customer_note: str = None,
    ):
        self.id = uuid.uuid4()
        self.items = items
        self.total_amount = total_amount
        self.delivery_address = delivery_address
        self.customer_note = customer_note
        self.status = "pending"
        self.placedAt = datetime.now()

    def confirm(self):
        """Mark the order as successfully placed."""
        self.status = "confirmed"

    def cancel(self):
        """Mark the order as canceled."""
        self.status = "canceled"
