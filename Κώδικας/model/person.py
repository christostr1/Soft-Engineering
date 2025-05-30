# model/person.py
import uuid
from model.errors import MissingNameError

class Person:
    def __init__(self, name: str):
        if not name or not name.strip():
            raise MissingNameError("Name is required")
        self.id = uuid.uuid4()
        self.name = name.strip()
