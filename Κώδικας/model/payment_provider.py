# model/payment_provider.py


class PaymentProvider:
    """
    Represents an external payment provider (e.g. Visa, PayPal).
    """

    def __init__(self, name: str, apiKey: str):
        self.name = name
        self.apiKey = apiKey

    def testConnection(self) -> bool:
        """
        Verify the API key / connection is valid.
        """
        # stub: always succeed
        return True

    def processTransaction(self, payment_method, amount: float) -> bool:
        """
        Attempt to charge `amount` using the given PaymentMethod.
        Return True on success, False on decline.
        """
        # In real life, call the provider’s SDK/API here.
        # Stub: accept any positive cvv except "000"
        if getattr(payment_method, "cvv", "") == "000":
            return False
        return True
