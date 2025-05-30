# model/errors.py


class MissingNameError(Exception):
    """Raised when the person’s name is empty."""

    pass


class InvalidEmailError(Exception):
    """Raised when an email address doesn’t match the pattern."""

    pass


class InvalidPhoneError(Exception):
    """Raised when a phone number is not in international format."""

    pass


class InvalidLicensePlateError(Exception):
    """Raised when license plate doesn’t match expected format."""

    pass


class WeakPasswordError(Exception):
    """Raised when password fails basic strength rules."""

    pass


# —— new for TC05 ——
class MissingLicensePlateError(Exception):
    """Raised when the license‐plate field is blank."""

    pass


class DuplicateEmailError(Exception):
    """Raised when trying to register with an email already in use."""

    pass


class MissingExperienceError(Exception):
    """Raised when the deliveryman’s experience field is left blank."""

    pass


class InvalidNameError(Exception):
    """Raised when the name contains invalid characters (e.g. digits)."""

    pass


class PaymentDeclinedError(Exception):
    """Raised when a payment provider refuses the transaction."""

    pass


class MissingPaymentMethodError(Exception):
    """Raised when no payment method was supplied for an order."""

    pass


class MissingAddressError(Exception):
    """Raised when no delivery address was provided."""

    pass
