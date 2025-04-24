# view/search_screen.py
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QPushButton
from view.components.base_screen import BaseScreen
from view.components.bottom_nav import BottomNav


class SearchScreen(BaseScreen):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Create a vertical layout for the screen
        layout = QVBoxLayout()

        # Title label for the Search Screen
        title = QLabel("SmartBite – Search Screen")
        layout.addWidget(title)

        # Button to navigate back to the Home Screen
        btn_back = QPushButton("Back to Home")
        # Set an object name to allow findChild to locate this button
        btn_back.setObjectName("navigate_to_home")
        layout.addWidget(btn_back)

        # Additional mock data or UI elements can be added here

        # Set the layout for this screen widget
        self.setLayout(layout)

        # Instead of adding BottomNav to the scroll content, create it as an overlay.
        # Make it a direct child of HomeScreen so it’s always visible.
        self.bottom_nav = BottomNav(current_tab="home", parent=self)
        # Set a fixed height for BottomNav (for example, 70 pixels)
        self.bottom_nav_height = 70
        self.bottom_nav.setFixedHeight(self.bottom_nav_height)
        self.bottom_nav.raise_()  # Ensure it is on top of the scroll area

        print("DEBUG: HomeScreen init completed")

    def resizeEvent(self, event):
        """
        Update the geometry of the bottom navigation bar so that it stays
        at the bottom of the HomeScreen while the scroll area fills the rest.
        """
        super().resizeEvent(event)
        # Get the full size of this widget.
        w = self.width()
        h = self.height()
        # Position BottomNav at bottom, with full width.
        self.bottom_nav.setGeometry(QRect(0, h - self.bottom_nav_height, w, self.bottom_nav_height))
