# model/filters.py
from dataclasses import dataclass

@dataclass
class Filters:
    max_price: float     # euros
    max_distance: float  # kilometers
    max_time: int        # minutes until meal
