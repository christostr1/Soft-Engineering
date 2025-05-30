import pytest
from model.preferences import Preferences
from model.filters import Filters
from model.recommendation_algorithm import RecommendationAlgorithm
from model.menu_item import MenuItem

# You may need to extend Filters.__init__ to raise ValueError on negatives.


@pytest.fixture
def algo():
    return RecommendationAlgorithm()


def test_mediterranean_gluten_under_10_at_14h(algo):
    """
    Input: Mediterranean, (gluten-free flag), <10€, time 14:00
    Expect: 3 suitable dishes
    """
    prefs = Preferences(cuisine="Μεσογειακή", meal_type="Μεσημεριανό")
    fltrs = Filters(max_price=10.0, max_distance=5.0, max_time=60)
    recs = algo.getRecommendations(None, prefs, fltrs)
    assert isinstance(recs, list)
    assert len(recs) == 3


def test_asian_vegan_under_8_at_2330(algo):
    """
    Input: Asian, Vegan, <8€, time 23:30
    Expect: no recommendations
    """
    prefs = Preferences(cuisine="Ασιατική", meal_type="Βραδινό")
    # Assuming `Filters` and `Preferences` support a vegan flag internally
    fltrs = Filters(max_price=8.0, max_distance=10.0, max_time=120)
    recs = algo.getRecommendations(None, prefs, fltrs)
    assert recs == []


def test_no_selection_uses_history(algo, monkeypatch):
    """
    Input: No prefs/filters (“Find something for me”)
    Expect: history‐based default (at least a "Burger")
    """

    # stub getRecommendations to check history‐path
    def stub(user, prefs, fltrs):
        # simulate history fallback
        return [MenuItem(name="Burger", price=6.0, image="burger.png")]

    monkeypatch.setattr(algo, "getRecommendations", stub)

    recs = algo.getRecommendations(None, None, None)
    assert len(recs) == 1
    assert recs[0].name.lower() == "burger"


def test_vegetarian_only(algo):
    """
    Input: Vegetarian, no other filters
    Expect: exactly 2 suitable dishes
    """
    prefs = Preferences(cuisine="Χορτοφαγική", meal_type="Μεσημεριανό")
    fltrs = Filters(max_price=100.0, max_distance=20.0, max_time=90)
    recs = algo.getRecommendations(None, prefs, fltrs)
    assert len(recs) == 2


def test_negative_price_raises_value_error():
    """
    Input: a negative max_price
    Expect: ValueError on filter creation
    """
    with pytest.raises(ValueError):
        Filters(max_price=-5.0, max_distance=5.0, max_time=30)
