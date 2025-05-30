import pytest
from model.delivery_person import DeliveryPerson
from model.errors import (
    MissingNameError,
    InvalidEmailError,
    InvalidPhoneError,
    InvalidLicensePlateError,
    WeakPasswordError,
)
from model.errors import DuplicateEmailError, MissingExperienceError, InvalidNameError


# --- A simple in-memory registry to test duplicate-email logic ---
class DummyRegistry:
    def __init__(self):
        self._by_email = {}

    def register(self, dp: DeliveryPerson):
        if dp.email in self._by_email:
            raise DuplicateEmailError("Account already exists")
        self._by_email[dp.email] = dp
        return True


@pytest.fixture
def registry():
    return DummyRegistry()


# 1) All fields correct → registration succeeds
def test_successful_registration(registry):
    dp = DeliveryPerson(
        name="Maria Papadopoulou",
        email="maria@example.com",
        phone="+301234567890",
        vehicle_type="Motorbike",
        license_plate="ABC-1234",
        password="Secret123!",
        experience=2,
    )
    assert registry.register(dp) is True


# 2) Missing license plate → rejection
def test_missing_license_plate():
    with pytest.raises(InvalidLicensePlateError):
        DeliveryPerson(
            name="Giannis Antetokounmpo",
            email="giannis@example.com",
            phone="+301234567891",
            vehicle_type="Van",
            license_plate="",  # <— missing
            password="Hoops2021",
            experience=5,
        )


# 3) Duplicate email → “account exists” error
def test_duplicate_email(registry):
    first = DeliveryPerson(
        name="Kostas Kar",
        email="kostas@example.com",
        phone="+301234567892",
        vehicle_type="Car",
        license_plate="DEF-5678",
        password="Drive123",
        experience=3,
    )
    registry.register(first)

    # second with same email
    second = DeliveryPerson(
        name="Dimitris Car",
        email="kostas@example.com",  # <— same email
        phone="+301234567893",
        vehicle_type="Car",
        license_plate="GHI-9012",
        password="Drive456",
        experience=4,
    )
    with pytest.raises(DuplicateEmailError) as exc:
        registry.register(second)
    assert "exists" in str(exc.value)


# 4) Missing experience → prompt for “experience” field
def test_missing_experience():
    with pytest.raises(MissingExperienceError):
        DeliveryPerson(
            name="Elena Rider",
            email="elena@example.com",
            phone="+301234567894",
            vehicle_type="Bicycle",
            license_plate="JKL-345",
            password="Bike123",
            experience=None,  # <— missing experience
        )


# 5) Name contains digits → invalid-name error
def test_name_with_numbers():
    with pytest.raises(InvalidNameError):
        DeliveryPerson(
            name="John123",  # <— digits in name
            email="john123@example.com",
            phone="+301234567895",
            vehicle_type="Motorbike",
            license_plate="MNO-7890",
            password="Moto1234",
            experience=1,
        )
