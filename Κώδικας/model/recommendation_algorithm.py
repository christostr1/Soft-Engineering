# model/recommendation_algorithm.py
import random
from typing import List
from model.preferences import Preferences
from model.filters import Filters
from model.menu_item import MenuItem
from model.person import Person
# from model.errors import CardExpiredError
# from model.geopoint import GeoPoint
from model.event_log import IEventRecorder, UserEvent


class RecommendationAlgorithm(IEventRecorder):
    def __init__(self):
        self.events: List[UserEvent] = []

    def record(self, e: UserEvent):
        self.events.append(e)

    def analyzeBehavior(self, user: Person):
        # stub: record login event
        self.record(UserEvent(type="login", timestamp=None))
        # possibly analyze past events here
        return

    def getRecommendations(
        self, user: Person, prefs: Preferences, fltrs: Filters
    ) -> List[MenuItem]:
        # In real life, call AI service here.
        # We'll just return 4 dummy MenuItems that roughly match filters.
        sample = [
            MenuItem(name="Greek Salad", price=5.0, image="salad.jpg"),
            MenuItem(name="Chicken Wrap", price=7.5, image="wrap.jpg"),
            MenuItem(name="Veggie Pizza", price=8.0, image="pizza.jpg"),
            MenuItem(name="Fruit Bowl", price=4.0, image="fruit.jpg"),
        ]
        # filter by max_price
        return [m for m in sample if m.price <= fltrs.max_price]
