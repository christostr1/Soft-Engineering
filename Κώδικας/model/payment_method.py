import uuid
from datetime import datetime


class CardExpiredError(Exception):
    pass


class MissingCVVError(Exception):
    pass


class InvalidCardNumberError(Exception):
    pass


class MissingCardHolderError(Exception):
    """Raised when the cardholder name is missing."""

    pass


class PaymentMethod:
    def __init__(self, holder: str, number: str, expiry: str, cvv: str):
        self.methodId = uuid.uuid4()
        self.holder = holder
        self.number = number.replace(" ", "")
        self.lastFour = self.number[-4:]
        self.expiry = expiry  # MM/YY
        self.cvv = cvv

    def masked_number(self):
        return f"**** **** **** {self.lastFour}"

    def validate(self):
        # 0) Holder name present
        if not self.holder or not self.holder.strip():
            raise MissingCardHolderError("Cardholder name is required")

        # 1) CVV present
        if not self.cvv:
            raise MissingCVVError("CVV is required")

        # 2) Number is numeric & length 16
        if not (self.number.isdigit() and len(self.number) == 16):
            raise InvalidCardNumberError("Card number must be 16 digits")

        # 3) Expiry valid and not in past
        try:
            exp = datetime.strptime(self.expiry, "%m/%y")
        except ValueError:
            raise ValueError("Expiry must be in MM/YY format")

        # approximate end-of-month check
        last_of_month = exp.replace(day=28)
        if last_of_month < datetime.now():
            raise CardExpiredError("Card expired")

        return True
