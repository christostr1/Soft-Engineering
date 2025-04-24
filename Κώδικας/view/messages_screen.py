import os
import logging

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea,
    QFrame, QToolButton, QSizePolicy
)
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from PyQt6.QtGui import QIcon, QFont, QPixmap
from config.settings import SETTINGS
from view.components.bottom_nav import BottomNav

class MessagesScreen(QWidget):
    """
    A screen displaying a chat/message list with a top bar,
    'All Message' subheading, and a scrollable list of chats.
    It includes a bottom navigation bar with 'messages' highlighted.
    """
    # Signal for the back button.
    backClicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        logging.debug("Initializing MessagesScreen.")
        self.setup_ui()

    def setup_ui(self):
        """Builds the UI for the messages screen."""
        # Main vertical layout filling the entire widget
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 1. Top Bar
        top_bar = self.create_top_bar()
        main_layout.addWidget(top_bar)

        # 2. Subheading: "All Message"
        subheading = self.create_subheading()
        main_layout.addWidget(subheading)

        # 3. Scroll Area for the messages list
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        content_widget = QFrame()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        # Add multiple chat items
        chats_section = self.create_chats_section()
        content_layout.addWidget(chats_section)

        # Add a stretch so that if there is extra space, items stay at the top
        content_layout.addStretch()

        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)

        # 4. Bottom Nav
        self.bottom_nav = BottomNav(current_tab="messages", parent=self)
        self.bottom_nav.setFixedHeight(70)
        self.bottom_nav.setStyleSheet(f"background-color: {SETTINGS['colors']['neutral']['Neutral 10']};")
        main_layout.addWidget(self.bottom_nav)

        self.setLayout(main_layout)
        logging.debug("MessagesScreen UI setup completed.")

    # --------------------------
    #     UI Helper Methods
    # --------------------------
    def create_top_bar(self) -> QWidget:
        """
        Creates a top bar with a back button on the left and a
        title "Chat List" in the center.
        """
        logging.debug("Creating top bar for MessagesScreen.")
        container = QFrame()
        container.setFixedHeight(56)
        layout = QHBoxLayout(container)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(0)

        # Back button
        btn_back = QToolButton()
        btn_back.setIcon(QIcon("resources/icons/Back2.png"))
        btn_back.setIconSize(QSize(32, 32))
        btn_back.setStyleSheet("border: none;")
        btn_back.clicked.connect(self.on_back_clicked)
        layout.addWidget(btn_back, alignment=Qt.AlignmentFlag.AlignLeft)

        # Title label
        title_label = QLabel("Chat List")
        title_label.setFont(QFont(SETTINGS["font_family"], 16, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #1E1E1E;")
        layout.addWidget(title_label, stretch=1, alignment=Qt.AlignmentFlag.AlignCenter)

        # Optionally add a placeholder right-side icon or spacing
        # layout.addStretch()

        return container

    def create_subheading(self) -> QWidget:
        """
        Creates a simple label "All Message" below the top bar.
        """
        logging.debug("Creating subheading for MessagesScreen.")
        container = QFrame()
        container.setFixedHeight(40)
        layout = QHBoxLayout(container)
        layout.setContentsMargins(16, 0, 16, 0)
        layout.setSpacing(0)

        subheading_label = QLabel("All Message")
        subheading_label.setFont(QFont(SETTINGS["font_family"], 14, QFont.Weight.Bold))
        subheading_label.setStyleSheet("color: #1E1E1E;")
        layout.addWidget(subheading_label, alignment=Qt.AlignmentFlag.AlignVCenter)

        return container

    def create_chats_section(self) -> QWidget:
        """
        Creates a vertical layout containing multiple chat item widgets
        that display user avatar, name, last message, time, and an unread/delivered indicator.
        """
        logging.debug("Creating chats section.")
        container = QFrame()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(16, 0, 16, 0)
        container_layout.setSpacing(12)

        # Sample chat items
        chat_items_data = [
            {
                "avatar": "resources/images/John.png",
                "name": "John Smith",
                "last_message": "Your Order Just Arrived!",
                "time": "13.47",
                "unread_or_check": "✓"  # or "3", etc.
            },
            {
                "avatar": "resources/images/John.png",
                "name": "John Smith",
                "last_message": "Your Order Just Arrived!",
                "time": "11.23",
                "unread_or_check": "3"
            },
            {
                "avatar": "resources/images/John.png",
                "name": "Janna Morgana",
                "last_message": "Your Order Just Arrived!",
                "time": "11.23",
                "unread_or_check": "✓"
            },
            {
                "avatar": "resources/images/John.png",
                "name": "John Smith",
                "last_message": "Your Order Just Arrived!",
                "time": "13.47",
                "unread_or_check": "✓"
            },
            {
                "avatar": "resources/images/John.png",
                "name": "John Smith",
                "last_message": "Your Order Just Arrived!",
                "time": "11.23",
                "unread_or_check": "1"
            },
            {
                "avatar": "resources/images/John.png",
                "name": "Janna Morgana",
                "last_message": "Your Order Just Arrived!",
                "time": "11.23",
                "unread_or_check": "✓"
            }
        ]

        for chat_data in chat_items_data:
            chat_item = self.create_chat_item(**chat_data)
            container_layout.addWidget(chat_item)

        return container

    def create_chat_item(self, avatar: str, name: str, last_message: str, time: str, unread_or_check: str) -> QWidget:
        """
        Creates a single chat item row with user avatar, name, last message,
        time, and an unread or check indicator.
        """
        item_container = QFrame()
        item_container.setFixedHeight(64)
        item_container.setStyleSheet("QFrame { background-color: transparent; }")
        layout = QHBoxLayout(item_container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        # Avatar
        avatar_label = QLabel()
        pixmap = QPixmap(avatar)
        if not pixmap.isNull():
            pixmap = pixmap.scaled(48, 48, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            avatar_label.setPixmap(pixmap)
        else:
            avatar_label.setText("No Image")
        avatar_label.setFixedSize(48, 48)
        layout.addWidget(avatar_label, alignment=Qt.AlignmentFlag.AlignVCenter)

        # Middle text (name + last message) in a vertical layout
        text_layout = QVBoxLayout()
        text_layout.setContentsMargins(0, 0, 0, 0)
        text_layout.setSpacing(2)

        name_label = QLabel(name)
        name_label.setFont(QFont(SETTINGS["font_family"], 14, QFont.Weight.Bold))
        name_label.setStyleSheet("color: #1E1E1E;")
        text_layout.addWidget(name_label)

        last_message_label = QLabel(last_message)
        last_message_label.setFont(QFont(SETTINGS["font_family"], 12))
        last_message_label.setStyleSheet("color: #9A9A9A;")
        text_layout.addWidget(last_message_label)

        layout.addLayout(text_layout, stretch=1)

        # Right side for time + unread/ delivered indicator
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(2)
        right_layout.setAlignment(Qt.AlignmentFlag.AlignRight)

        time_label = QLabel(time)
        time_label.setFont(QFont(SETTINGS["font_family"], 12))
        time_label.setStyleSheet("color: #9A9A9A;")
        time_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        right_layout.addWidget(time_label)

        # Orange indicator: either a check mark or a badge
        unread_label = QLabel(unread_or_check)
        unread_label.setFont(QFont(SETTINGS["font_family"], 10, QFont.Weight.Bold))
        unread_label.setFixedWidth(20)
        unread_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        unread_label.setStyleSheet("""
            QLabel {
                color: white;
                background-color: #FE8C00;
                border-radius: 10px;
                padding: 2px 4px;
                qproperty-alignment: 'AlignCenter';
            }
        """)
        right_layout.addWidget(unread_label, alignment=Qt.AlignmentFlag.AlignRight)

        layout.addLayout(right_layout)

        return item_container

    # -------------------------
    #     Logic Methods
    # -------------------------
    def on_back_clicked(self):
        """
        Called when the top bar's back button is pressed.
        Emit backClicked so the controller or main app can navigate.
        """
        logging.debug("MessagesScreen: Back button clicked.")
        self.backClicked.emit()
