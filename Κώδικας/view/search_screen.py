# view/search_screen.py
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QLineEdit,
    QFrame,
    QScrollArea,
    QCheckBox,
    QToolButton,
    QSpinBox,
    QSizePolicy,
)
from PyQt6.QtGui import QFont, QIcon, QPixmap
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from config.settings import SETTINGS
import logging
import os
from view.components.category_widget import CategoryWidget


class SearchScreen(QWidget):
    # signals for navigation & interaction
    back = pyqtSignal()
    search = pyqtSignal(str)
    filterClicked = pyqtSignal()
    categorySelected = pyqtSignal(str)
    recentSearchRemoved = pyqtSignal(str)
    deleteAllRecent = pyqtSignal()
    orderSelected = pyqtSignal(dict)

    def __init__(self, parent=None, recent_searches=None, recent_orders=None):
        super().__init__(parent)

        # default data if none passed
        self.recent_searches = recent_searches or [
            "Burgers",
            "Fast food",
            "Dessert",
            "French",
            "Fastry",
        ]
        self.recent_orders = recent_orders or [
            {
                "name": "Ordinary Burgers",
                "subtitle": "Burger Restaurant",
                "rating": "4.9",
                "distance": "190m",
                "image": "resources/images/smoked_burger.png",
            },
            {
                "name": "Ordinary Burgers",
                "subtitle": "Burger Restaurant",
                "rating": "4.9",
                "distance": "190m",
                "image": "resources/images/smoked_burger.png",
            },
            {
                "name": "Ordinary Burgers",
                "subtitle": "Burger Restaurant",
                "rating": "4.9",
                "distance": "190m",
                "image": "resources/images/smoked_burger.png",
            },
            {
                "name": "Ordinary Burgers",
                "subtitle": "Burger Restaurant",
                "rating": "4.9",
                "distance": "190m",
                "image": "resources/images/smoked_burger.png",
            },
        ]

        self._build_ui()

    def _build_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ─── Header ────────────────────────────────────────────────────────────
        header = QHBoxLayout()
        header.setContentsMargins(16, 16, 16, 0)

        # Back Button.
        back_btn = QPushButton()
        back_btn.setIcon(QIcon("resources/icons/Back2.png"))
        back_btn.setIconSize(QSize(40, 40))
        back_btn.setStyleSheet("border: none;")
        back_btn.clicked.connect(lambda: self.back.emit())
        header.addWidget(back_btn)

        # Title label (centered).
        title_label = QLabel("Search Food")
        title_label.setFont(QFont(SETTINGS["font_family"], 16, QFont.Weight.Bold))
        title_label.setStyleSheet(
            f"color: {SETTINGS['colors']['neutral']['Neutral 100']};"
        )
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.addWidget(title_label, stretch=1)

        # placeholder to keep title centered
        placeholder = QToolButton()
        placeholder.setFixedSize(QSize(40, 40))
        placeholder.setVisible(False)
        header.addWidget(placeholder, alignment=Qt.AlignmentFlag.AlignRight)

        main_layout.addLayout(header)

        # ─── Search Bar ────────────────────────────────────────────────────────
        search_layout = QHBoxLayout()
        search_layout.setContentsMargins(16, 8, 16, 8)

        search_input = QLineEdit()
        search_input.setPlaceholderText("Search Food")
        search_input.setFixedHeight(40)
        search_input.setStyleSheet(
            """
            QLineEdit {
                background-color: #FFFFFF;
                border: 1px solid #EEE;
                border-radius: 12px;
                padding-left: 12px;
                font-size: 14px;
            }
            QLineEdit:placeholder {
                color: #000;
            }
        """
        )
        search_input.returnPressed.connect(
            lambda: self.search.emit(search_input.text())
        )

        search_layout.addWidget(search_input)
        main_layout.addLayout(search_layout)

        # ─── Scrollable Content ────────────────────────────────────────────────
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        content = QVBoxLayout(container)
        content.setContentsMargins(16, 0, 16, 16)
        content.setSpacing(16)

        # —— Categories Row

        categories = [
            ("resources/images/burger.png", "Burger", True),
            ("resources/images/taco.png", "Taco", False),
            ("resources/images/drink.png", "Drink", False),
            ("resources/images/pizza.png", "Pizza", False),
        ]

        category_widget = CategoryWidget(categories)
        content.addWidget(category_widget)

        # —— Recent searches header
        rs_header = QHBoxLayout()
        rs_label = QLabel("Recent searches")
        rs_label.setFont(QFont(SETTINGS["font_family"], 12, QFont.Weight.Bold))
        rs_label.setStyleSheet(
            f"""
              color: {SETTINGS['colors']['neutral']['Neutral 100']};
              background: transparent;
            """
        )
        rs_delete = QPushButton("Delete")
        rs_delete.setStyleSheet(
            f"""
                color: {SETTINGS['colors']['primary']['hover']};
                background: transparent;
                border: none;
                font-size: 13px;
            """
        )
        rs_delete.clicked.connect(lambda: self.deleteAllRecent.emit())
        rs_header.addWidget(rs_label)
        rs_header.addStretch()
        rs_header.addWidget(rs_delete)
        content.addLayout(rs_header)

        script_dir = os.path.dirname(os.path.abspath(__file__))
        search_icon_path = os.path.join(
            script_dir, "..", "resources", "icons", "search2.png"
        )

        # —— Recent searches list
        for term in self.recent_searches:
            row = QHBoxLayout()

            search_icon_label = QLabel()
            search_icon_label.setPixmap(QPixmap(search_icon_path))
            # search_icon_label.setFixedSize(20, 20)

            row.addWidget(search_icon_label)
            lbl = QLabel(term)
            lbl.setFont(QFont(SETTINGS["font_family"], 12))
            lbl.setStyleSheet(
                """
                  color: #101010;
                """
            )
            row.addWidget(lbl)
            row.addStretch()
            remove_btn = QPushButton("✕")
            remove_btn.setStyleSheet(
                """
                QPushButton {
                  color: #878787;
                  border: none;
                  background: transparent;
                  font-size: 14px;
                }
            """
            )
            remove_btn.clicked.connect(
                lambda _, t=term: self.recentSearchRemoved.emit(t)
            )
            row.addWidget(remove_btn)
            content.addLayout(row)

        # —— Separator
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setFrameShadow(QFrame.Shadow.Sunken)
        content.addWidget(sep)

        # —— Recent orders header
        ro_label = QLabel("My recent orders")
        ro_label.setFont(QFont(SETTINGS["font_family"], 14, QFont.Weight.Bold))
        ro_label.setStyleSheet(
            f"""
              color: {SETTINGS['colors']['neutral']['Neutral 100']};
              background: transparent;
            """
        )
        content.addWidget(ro_label)

        # —— Recent orders list
        for order in self.recent_orders:
            item = QFrame()
            item.setStyleSheet(
                f"""
                    color: {SETTINGS['colors']['neutral']['Neutral 100']};
                    background: transparent;
                """
            )
            item.setFixedHeight(80)
            hl = QHBoxLayout(item)
            pix = QPixmap(order["image"]).scaled(
                60,
                60,
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation,
            )
            img = QLabel()
            img.setPixmap(pix)
            img.setFixedSize(60, 60)
            img.setStyleSheet("border-radius: 8px;")
            hl.addWidget(img)

            vtxt = QVBoxLayout()
            name = QLabel(order["name"])
            name.setFont(QFont(SETTINGS["font_family"], 13))
            vtxt.addWidget(name)
            sub = QLabel(order["subtitle"])
            sub.setFont(QFont(SETTINGS["font_family"], 11))

            sub.setStyleSheet(
                f"""
                    color: {SETTINGS['colors']['neutral']['Neutral 60']};
                    background: transparent;
                """
            )
            vtxt.addWidget(sub)

            stats = QHBoxLayout()
            rating = order["rating"]
            rating_widget = self.create_info_item("resources/icons/star.png", rating)
            stats.addWidget(rating_widget)
            distance = order["distance"]
            distance_widget = self.create_info_item(
                "resources/icons/location.png", distance
            )
            stats.addWidget(distance_widget)
            stats.addStretch()
            vtxt.addLayout(stats)

            hl.addLayout(vtxt)
            hl.addStretch()

            # click anywhere on the row to select
            item.mousePressEvent = lambda e, o=order: self.orderSelected.emit(o)
            content.addWidget(item)

        scroll.setWidget(container)
        main_layout.addWidget(scroll)

    def create_info_item(self, icon_path: str, text: str) -> QWidget:
        """
        Helper method to create a widget that combines an icon and text.
        """
        container = QFrame()
        item_layout = QHBoxLayout(container)
        item_layout.setContentsMargins(0, 0, 0, 0)
        item_layout.setSpacing(4)

        icon_label = QLabel()
        pixmap = QPixmap(icon_path)
        pixmap = pixmap.scaled(
            16,
            16,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        icon_label.setPixmap(pixmap)
        icon_label.setFixedSize(16, 16)
        item_layout.addWidget(icon_label)

        text_label = QLabel(text)
        text_label.setFont(QFont(SETTINGS["font_family"], 10))
        text_label.setStyleSheet(
            f"color: {SETTINGS['colors']['neutral']['Neutral 100']};"
        )
        item_layout.addWidget(text_label)

        return container
