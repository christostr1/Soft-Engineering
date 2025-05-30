# model/menu_item.py
from dataclasses import dataclass


@dataclass
class MenuItem:
    name: str
    price: float
    image: str  # just the filename under resources/images/
