import pytest
from model.menu_item import MenuItem
from model.payment_method import PaymentMethod
from model.payment_provider import PaymentProvider
from service.order_service import OrderService
from model.errors import (
    PaymentDeclinedError,
    MissingPaymentMethodError,
    MissingAddressError,
)


@pytest.fixture
def items():
    # dummy menu items by name
    return [MenuItem(name="Burger", price=5.0, image="burger.png")]


@pytest.fixture
def valid_card():
    pm = PaymentMethod(
        holder="Alice", number="4111111111111111", expiry="12/30", cvv="123"
    )
    # mark as default and attach a Visa provider stub
    pm.is_default = True
    pm.provider = PaymentProvider(name="Visa", apiKey="key")
    return pm


@pytest.fixture
def invalid_cvv_card():
    # CVV will be rejected by provider stub
    pm = PaymentMethod(
        holder="Bob", number="4111111111111111", expiry="12/30", cvv="000"
    )
    pm.is_default = True
    pm.provider = PaymentProvider(name="Visa", apiKey="key")
    return pm


@pytest.fixture
def paypal_account():
    pm = PaymentMethod(
        holder="Carol", number="", expiry="", cvv=""
    )  # number empty for PayPal
    pm.is_default = True
    pm.provider = PaymentProvider(name="PayPal", apiKey="key")
    return pm


@pytest.fixture(autouse=True)
def stub_providers(monkeypatch):
    # stub Visa: decline when cvv == "000"
    def process_transaction_visa(amount):
        if process_transaction_visa.last_cvv == "000":
            return False
        return True

    def stub_process(self):
        process_transaction_visa.last_cvv = self.cvv
        return process_transaction_visa(self)

    monkeypatch.setattr(
        PaymentProvider, "processTransaction", lambda self, pm, amt: stub_process(pm)
    )
    # stub PayPal to always succeed
    monkeypatch.setattr(
        PaymentProvider, "processTransaction", lambda self, pm, amt: True
    )


def test_successful_order_with_card_and_address(items, valid_card):
    order = OrderService.place_order(
        items=items, payment_method=valid_card, address="Παγκράτι", note=None
    )
    assert order.status == "confirmed"
    assert order.delivery_address == "Παγκράτι"


def test_payment_declined_with_invalid_cvv(items, invalid_cvv_card):
    with pytest.raises(PaymentDeclinedError):
        OrderService.place_order(
            items=items, payment_method=invalid_cvv_card, address="Κολωνάκι", note=None
        )


def test_successful_order_with_paypal_and_note(items, paypal_account):
    order = OrderService.place_order(
        items=items,
        payment_method=paypal_account,
        address="Γλυφάδα",
        note="Χωρίς wasabi",
    )
    assert order.status == "confirmed"
    assert order.customer_note == "Χωρίς wasabi"


def test_missing_payment_method(items):
    with pytest.raises(MissingPaymentMethodError):
        OrderService.place_order(
            items=items, payment_method=None, address="Ψυχικό", note=None
        )


def test_missing_address(items, valid_card):
    with pytest.raises(MissingAddressError):
        OrderService.place_order(
            items=items, payment_method=valid_card, address="", note=None
        )
