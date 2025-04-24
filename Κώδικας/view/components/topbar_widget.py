# view/components/topbar_widget.py

import os

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QComboBox, QVBoxLayout, QFrame
from PyQt6.QtGui import QFont, QIcon, QPainter, QPixmap
from PyQt6.QtCore import Qt, QSize
from config.settings import SETTINGS


class TopBarWidget(QWidget):
    """
    The top bar contains the user's location,
    a dropdown for changing location, and search/bell icons.
    This widget draws a background image by overriding paintEvent.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(220)

        # Compute the absolute path to the background image.
        # __file__ is in 'components', so we go up two levels to resources/images/
        script_dir = os.path.dirname(os.path.abspath(__file__))
        bg_path = os.path.join(script_dir, "..", "..", "resources", "images", "topbar_bg.png")
        self.bg_pixmap = QPixmap(bg_path)

        # Create a foreground container for holding UI elements (transparent, so background shows through)
        self.foreground = QFrame(self)
        self.foreground.setStyleSheet("background: transparent;")
        self.foreground.setGeometry(self.rect())  # Initially fill the entire widget

        # Set up the layout for the foreground container.
        foreground_layout = QVBoxLayout(self.foreground)
        foreground_layout.setContentsMargins(10, 10, 10, 10)
        foreground_layout.setSpacing(10)

        # --- Top Row ---
        top_row = QHBoxLayout()
        top_row.setContentsMargins(0, 0, 0, 0)

        # Left side: Location column with a label and dropdown.
        location_col = QVBoxLayout()
        location_label = QLabel("Your Location")
        location_label.setStyleSheet(f"""
            font-size: 14px;
            color: {SETTINGS['colors'].get('neutral', {}).get('Neutral 10', '#CCCCCC')};
            border: none;
        """)
        location_dropdown = QComboBox()
        location_dropdown.addItems(["Patras", "Athens", "Thessaloniki"])
        location_dropdown.setStyleSheet(f"""
            font-size: {SETTINGS['font_size_default']}px;
            color: {SETTINGS['colors'].get('neutral', {}).get('Neutral 10', '#CCCCCC')};
            background-color: transparent;
            border: none;
        """)
        location_col.addWidget(location_label)
        location_col.addWidget(location_dropdown)
        top_row.addLayout(location_col)
        top_row.addStretch()

        # Right side: Icons (search and bell)
        icon_search = QPushButton()
        search_icon_path = os.path.join(script_dir, "..", "..", "resources", "icons", "search.png")
        icon_search.setIcon(QIcon(search_icon_path))
        icon_search.setIconSize(QSize(24, 24))
        icon_search.setFixedSize(36, 36)
        icon_search.setStyleSheet("border: none; background-color: transparent;")

        icon_bell = QPushButton()
        bell_icon_path = os.path.join(script_dir, "..", "..", "resources", "icons", "bell.png")
        icon_bell.setIcon(QIcon(bell_icon_path))
        icon_bell.setIconSize(QSize(24, 24))
        icon_bell.setFixedSize(36, 36)
        icon_bell.setStyleSheet("border: none; background-color: transparent;")

        top_row.addWidget(icon_search)
        top_row.addWidget(icon_bell)
        foreground_layout.addLayout(top_row)

        # Spacer to push the headline down
        foreground_layout.addStretch()

        # Headline label at the bottom of the top bar
        headline = QLabel("Provide the best\nfood for you")
        headline.setFont(QFont("Inter", 30, QFont.Weight.Bold))
        headline.setStyleSheet("color: white;")
        headline.setWordWrap(True)
        foreground_layout.addWidget(headline)

    def resizeEvent(self, event):
        # Ensure the foreground container always covers the entire TopBarWidget.
        self.foreground.setGeometry(self.rect())
        super().resizeEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        if not self.bg_pixmap.isNull():
            # Scale the background pixmap to cover the widget.
            # KeepAspectRatioByExpanding scales the image while preserving aspect ratio.
            scaled = self.bg_pixmap.scaled(
                self.size(),
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation,
            )
            # Center the scaled pixmap.
            x = (self.width() - scaled.width()) // 2
            y = (self.height() - scaled.height()) // 2
            painter.drawPixmap(x, y, scaled)
        else:
            print("Background pixmap is null. Check the image path!")

