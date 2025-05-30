# model/delivery_person.py
import re
import uuid
import hashlib
from model.person import Person
from model.geopoint import GeoPoint
from model.errors import (
    MissingNameError,
    InvalidEmailError,
    InvalidPhoneError,
    InvalidLicensePlateError,
    WeakPasswordError,
    MissingExperienceError,
    InvalidNameError,
)


class DeliveryPerson(Person):
    def __init__(
        self,
        name: str,
        email: str,
        phone: str,
        vehicle_type: str,
        license_plate: str,
        password: str,
        experience,
    ):
        super().__init__(name)
        # 0) Name must not contain digits
        if any(ch.isdigit() for ch in self.name):
            raise InvalidNameError("Name must not contain numbers")
        self.email = email.strip()
        self.phone = phone.strip().replace(" ", "")
        self.vehicle_type = vehicle_type
        self.license_plate = license_plate.strip().upper()
        self.password_hash = self._hash_password(password)
        self.currentLocation: GeoPoint | None = None
        self.experience = experience

        # 1) Experience must be provided
        if experience is None or (
            isinstance(experience, str) and not experience.strip()
        ):
            raise MissingExperienceError("Experience is required")
        # (optionally you could also check numeric > 0)
        # Validation
        self._validate_email()
        self._validate_phone()
        self._validate_license_plate()
        self._validate_password(password)

    def _hash_password(self, password: str) -> str:
        # Simple SHA256; swap in bcrypt for production
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    def _validate_email(self):
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(pattern, self.email):
            raise InvalidEmailError("Invalid email address")

    def _validate_phone(self):
        # Expect +[country][number], 10–15 digits
        if not re.match(r"^\+\d{10,15}$", self.phone):
            raise InvalidPhoneError("Invalid phone number")

    def _validate_license_plate(self):
        # e.g. ABC-1234 or AB-123
        if not re.match(r"^[A-Z]{2,3}-\d{1,4}$", self.license_plate):
            raise InvalidLicensePlateError("Invalid license plate format")

    def _validate_password(self, password: str):
        if len(password) < 8:
            raise WeakPasswordError("Password must be ≥8 characters")
        if not re.search(r"\d", password):
            raise WeakPasswordError("Password must include a digit")
        if not re.search(r"[A-Za-z]", password):
            raise WeakPasswordError("Password must include a letter")

    # --- Your class‐diagram methods ---
    def acceptOrder(self, order: "Order"):
        print(f"DeliveryPerson {self.id} accepted order {order.id}")

    def rejectOrder(self, order: "Order"):
        print(f"DeliveryPerson {self.id} rejected order {order.id}")

    def updateLocation(self, loc: GeoPoint):
        self.currentLocation = loc
        print(f"DeliveryPerson {self.id} location set to {loc}")
