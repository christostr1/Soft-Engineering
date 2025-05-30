# tests/test_menu_update.py

import os
import pytest

from model.menu_item import MenuItem
from service.menu_service import add_menu_item
from model.errors import (
    MissingDescriptionError,
    InvalidPriceError,
    ImageTooLargeError,
)


@pytest.fixture
def small_image(tmp_path):
    """Create a dummy image file of size 3 MB."""
    path = tmp_path / "small.jpg"
    path.write_bytes(b"\x00" * (3 * 1024 * 1024))
    return str(path)


@pytest.fixture
def large_image(tmp_path):
    """Create a dummy image file of size 6 MB."""
    path = tmp_path / "large.jpg"
    path.write_bytes(b"\x00" * (6 * 1024 * 1024))
    return str(path)


def test_add_valid_dish(small_image):
    """
    Input: 'Καρμπονάρα', description, 7.90€, 'Ζυμαρικά'
    Expected: MenuItem instance returned
    """
    item = add_menu_item(
        title="Καρμπονάρα",
        description="Κλασική ιταλική καρμπονάρα με μπέικον και καπαρντίνα.",
        price=7.90,
        category="Ζυμαρικά",
        image_path=small_image,
    )
    assert isinstance(item, MenuItem)
    assert item.name == "Καρμπονάρα"
    assert pytest.approx(item.price, 0.01) == 7.90
    assert item.category == "Ζυμαρικά"


def test_missing_description_raises(small_image):
    """
    Input: 'Σαλάτα', without description
    Expected: MissingDescriptionError
    """
    with pytest.raises(MissingDescriptionError):
        add_menu_item(
            title="Σαλάτα",
            description="",
            price=5.00,
            category="Χορτοφαγικά",
            image_path=small_image,
        )


def test_negative_price_rejected(small_image):
    """
    Input: 'Χυλός', price -2€
    Expected: InvalidPriceError
    """
    with pytest.raises(InvalidPriceError):
        add_menu_item(
            title="Χυλός",
            description="Πρωινό χυλός με μέλι.",
            price=-2.00,
            category="Πρωινό",
            image_path=small_image,
        )


def test_image_too_large_rejected(large_image):
    """
    Input: any title/description/price, image >5MB
    Expected: ImageTooLargeError
    """
    with pytest.raises(ImageTooLargeError):
        add_menu_item(
            title="Πίτσα Καπριτσιόζα",
            description="Με ποικιλία τυριών.",
            price=9.50,
            category="Πίτσες",
            image_path=large_image,
        )


def test_title_with_emoji_allowed(small_image):
    """
    Input: '🍕 Special', description, 8.00€, category
    Expected: succeeds despite emoji in title
    """
    item = add_menu_item(
        title="🍕 Special",
        description="Πίτσα με extra τυρί.",
        price=8.00,
        category="Πίτσες",
        image_path=small_image,
    )
    assert isinstance(item, MenuItem)
    assert item.name == "🍕 Special"
