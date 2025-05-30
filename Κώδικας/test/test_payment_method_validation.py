import pytest
from datetime import datetime, timedelta

from model.payment_method import (
    PaymentMethod,
    CardExpiredError,
    MissingCVVError,
    InvalidCardNumberError,
    MissingCardHolderError,
)
import sys, os
# Insert your project root (one level up from test/) onto sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def test_validate_success_future_expiry():
    pm = PaymentMethod(holder="John Doe",
                       number="4111111111111111",
                       expiry="12/30",
                       cvv="123")
    assert pm.validate() is True

def test_validate_missing_holder():
    pm = PaymentMethod(holder="   ",
                       number="4111111111111111",
                       expiry="12/30",
                       cvv="123")
    with pytest.raises(MissingCardHolderError) as exc:
        pm.validate()
    assert "Cardholder name is required" in str(exc.value)

def test_validate_missing_cvv():
    pm = PaymentMethod(holder="Jane Doe",
                       number="4111111111111111",
                       expiry="12/30",
                       cvv="")
    with pytest.raises(MissingCVVError) as exc:
        pm.validate()
    assert "CVV is required" in str(exc.value)

def test_validate_invalid_number():
    pm = PaymentMethod(holder="Jane Doe",
                       number="1234 5678",  # too short / non‐numeric
                       expiry="12/30",
                       cvv="123")
    with pytest.raises(InvalidCardNumberError) as exc:
        pm.validate()
    assert "Card number must be 16 digits" in str(exc.value)

def test_validate_expired_card():
    past = (datetime.now() - timedelta(days=365)).strftime("%m/%y")
    pm = PaymentMethod(holder="John Doe",
                       number="4111111111111111",
                       expiry=past,
                       cvv="123")
    with pytest.raises(CardExpiredError) as exc:
        pm.validate()
    assert "Card expired" in str(exc.value)

def test_validate_bad_expiry_format():
    pm = PaymentMethod(holder="John Doe",
                       number="4111111111111111",
                       expiry="bad-format",
                       cvv="123")
    with pytest.raises(ValueError) as exc:
        pm.validate()
    assert "Expiry must be in MM/YY format" in str(exc.value)
