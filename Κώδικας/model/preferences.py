# model/preferences.py
from dataclasses import dataclass


@dataclass
class Preferences:
    cuisine: str  # e.g. "Μεσογειακή"
    meal_type: str  # e.g. "Μεσημεριανό"
