# view/home_screen.py
import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QFrame
from PyQt6.QtCore import Qt, QRect
from config.settings import SETTINGS
from view.components.topbar_widget import TopBarWidget
from view.components.category_widget import CategoryWidget
from view.components.product_grid import ProductGrid
from view.components.bottom_nav import BottomNav


class HomeScreen(QWidget):
    """
    The main home screen showing a top bar, category carousel, product grid.
    The content scrolls, and the bottom navigation bar is overlaid at the bottom.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        print("DEBUG: HomeScreen init")

        # Overall main layout fills the widget.
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Create scroll area for all the content.
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # Content widget with its layout.
        self.content_widget = QFrame()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(0)

        # TopBar widget (with background image, location, and icons)
        top_bar = TopBarWidget()
        self.content_layout.addWidget(top_bar)

        # Category Widget with placeholder categories.
        categories = [
            ("resources/images/burger.png", "Burger", True),
            ("resources/images/taco.png", "Taco", False),
            ("resources/images/drink.png", "Drink", False),
            ("resources/images/pizza.png", "Pizza", False)
        ]
        self.category_widget = CategoryWidget(categories)
        self.content_layout.addWidget(self.category_widget)

        # Product Grid: sample product data passed as a list of dictionaries.
        products = [
            {
                "image": "resources/images/smoked_burger.png",
                "title": "Smoked Burger",
                "rating": "4.5",
                "distance": "1.2km",
                "price": "$10.00"
            },
            {
                "image": "resources/images/classic_burger.png",
                "title": "Classic Burger",
                "rating": "4.7",
                "distance": "2.0km",
                "price": "$9.50"
            },
            {
                "image": "resources/images/smoked_burger.png",
                "title": "Smoked Burger",
                "rating": "4.5",
                "distance": "1.2km",
                "price": "$10.00"
            },
            {
                "image": "resources/images/classic_burger.png",
                "title": "Classic Burger",
                "rating": "4.7",
                "distance": "2.0km",
                "price": "$9.50"
            }
        ]
        self.product_grid = ProductGrid(products)
        self.content_layout.addWidget(self.product_grid)

        # IMPORTANT: Add bottom padding to the content layout so that the last elements
        # are not hidden behind the bottom nav.
        self.content_layout.addStretch(1)
        self.content_layout.setContentsMargins(0, 0, 0, 10)  # 70px bottom padding; adjust as needed.

        # Set the content widget in the scroll area.
        self.scroll_area.setWidget(self.content_widget)

        # Add the scroll area to the main layout.
        self.main_layout.addWidget(self.scroll_area)

        # ----- Bottom Navigation (Fixed) -----
        # Create the BottomNav widget with a fixed height and a non-transparent background.
        self.bottom_nav = BottomNav(current_tab="home", parent=self)
        self.bottom_nav.setFixedHeight(70)
        # Update its stylesheet to have a solid background color. You can refer to your settings.
        self.bottom_nav.setStyleSheet(f"background-color: {SETTINGS['colors']['neutral']['Neutral 10']};")
        # Add the bottom nav at the bottom of the main layout.
        self.main_layout.addWidget(self.bottom_nav)

        print("DEBUG: HomeScreen init completed")
        self.setLayout(self.main_layout)

