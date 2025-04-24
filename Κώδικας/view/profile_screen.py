import logging
import os

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea,
    QFrame, QToolButton, QPushButton, QSizePolicy
)
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from PyQt6.QtGui import QIcon, QFont, QPixmap
from config.settings import SETTINGS
from view.components.bottom_nav import BottomNav

class ProfileScreen(QWidget):
    """
    A screen replicating the Profile Settings design:
    - Top bar with a back button
    - User avatar, name, and email
    - My Orders section with order card
    - Profile options list
    - Sign Out button
    - Bottom navigation with "profile" tab highlighted
    """
    backClicked = pyqtSignal()  # Emitted when the back button is pressed

    def __init__(self, parent=None):
        super().__init__(parent)
        logging.debug("Initializing ProfileScreen.")
        self.setup_ui()

    def setup_ui(self):
        """Builds the entire UI layout for the profile screen."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 1. Top bar
        top_bar = self.create_top_bar()
        main_layout.addWidget(top_bar)

        # 2. Scrollable content
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        content_widget = QFrame()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        # 2a. User Info
        user_info = self.create_user_info()
        content_layout.addWidget(user_info)

        # 2b. My Orders section
        orders_section = self.create_orders_section()
        content_layout.addWidget(orders_section)

        # 2c. Profile Options
        profile_options = self.create_profile_options()
        content_layout.addWidget(profile_options)

        # 2d. Sign Out Button
        sign_out_btn = self.create_sign_out_button()
        content_layout.addWidget(sign_out_btn)

        # Add stretch at the end so content doesn't crowd the bottom
        content_layout.addStretch()

        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)

        # 3. Bottom Navigation
        self.bottom_nav = BottomNav(current_tab="profile", parent=self)
        self.bottom_nav.setFixedHeight(70)
        # For a non-transparent background
        self.bottom_nav.setStyleSheet(f"background-color: {SETTINGS['colors']['neutral']['Neutral 10']};")

        main_layout.addWidget(self.bottom_nav)

        self.setLayout(main_layout)
        logging.debug("ProfileScreen UI setup completed.")

    # ---------------------------------
    #    UI Construction Methods
    # ---------------------------------

    def create_top_bar(self) -> QWidget:
        """
        Creates a top bar with a back button on the left
        and a title "Profile Settings" in the center.
        """
        logging.debug("Creating top bar for ProfileScreen.")
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

        # Title
        title_label = QLabel("Profile Settings")
        title_label.setFont(QFont(SETTINGS["font_family"], 16, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #1E1E1E;")
        layout.addWidget(title_label, stretch=1, alignment=Qt.AlignmentFlag.AlignCenter)

        # Right side spacing (or extra button if needed)
        # layout.addStretch()

        return container

    def on_back_clicked(self):
        """
        Called when the back button is clicked.
        Emits a signal so that the navigation logic can be handled externally.
        """
        logging.debug("ProfileScreen: Back button clicked.")
        self.backClicked.emit()

    def create_user_info(self) -> QWidget:
        """
        Creates the user avatar, name, and email section.
        """
        logging.debug("Creating user info section.")
        container = QFrame()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(16, 16, 16, 16)
        container_layout.setSpacing(8)

        # Avatar row
        avatar_layout = QHBoxLayout()
        avatar_layout.setSpacing(16)

        avatar_label = QLabel()
        # Placeholder user avatar
        pixmap = QPixmap("resources/images/profile_avatar.png")
        if not pixmap.isNull():
            pixmap = pixmap.scaled(80, 80, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            avatar_label.setPixmap(pixmap)
        else:
            avatar_label.setText("No Image")
        avatar_label.setFixedSize(80, 80)
        avatar_layout.addWidget(avatar_label, alignment=Qt.AlignmentFlag.AlignCenter)

        container_layout.addLayout(avatar_layout)

        # User Name
        name_label = QLabel("Zed Zilean")
        name_label.setFont(QFont(SETTINGS["font_family"], 16, QFont.Weight.Bold))
        name_label.setStyleSheet("color: #1E1E1E;")
        name_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        container_layout.addWidget(name_label)

        # Email
        email_label = QLabel("zedzilean@gmail.com")
        email_label.setFont(QFont(SETTINGS["font_family"], 12))
        email_label.setStyleSheet("color: #9A9A9A;")
        email_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        container_layout.addWidget(email_label)

        return container

    def create_orders_section(self) -> QWidget:
        """
        Creates the 'My Orders' section with:
          - Title 'My Orders'
          - 'See All' button
          - A sample order card
        """
        logging.debug("Creating orders section.")
        container = QFrame()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(16, 16, 16, 16)
        container_layout.setSpacing(12)

        # Header row: "My Orders" + "See All" + status
        header_layout = QHBoxLayout()
        title_label = QLabel("My Orders")
        title_label.setFont(QFont(SETTINGS["font_family"], 14, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #1E1E1E;")
        header_layout.addWidget(title_label)

        header_layout.addStretch()

        see_all_button = QPushButton("See All")
        see_all_button.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #FE8C00;
                border: none;
            }
        """)
        see_all_button.setFont(QFont(SETTINGS["font_family"], 12))
        # Connect if needed: see_all_button.clicked.connect(...)
        header_layout.addWidget(see_all_button)

        container_layout.addLayout(header_layout)

        # Order Card
        order_card = self.create_order_card()
        container_layout.addWidget(order_card)

        return container

    def create_order_card(self) -> QWidget:
        """
        Creates a placeholder order card with:
         - Order ID
         - Status (In Delivery)
         - Product image, name, price, items
        """
        card_container = QFrame()
        card_container.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border-radius: 12px;
            }
        """)
        layout = QVBoxLayout(card_container)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(8)

        # 1) Row: order ID and status badge
        row1_layout = QHBoxLayout()

        lbl_order_id = QLabel("Order ID 88833777")
        lbl_order_id.setFont(QFont(SETTINGS["font_family"], 12))
        lbl_order_id.setStyleSheet("color: #646464;")
        row1_layout.addWidget(lbl_order_id)

        row1_layout.addStretch()

        status_label = QLabel("In Delivery")
        status_label.setFont(QFont(SETTINGS["font_family"], 12, QFont.Weight.Bold))
        status_label.setFixedHeight(24)
        status_label.setStyleSheet("""
            QLabel {
                background-color: #FE8C00;
                color: white;
                border-radius: 12px;
                padding: 0 8px;
            }
        """)
        row1_layout.addWidget(status_label, alignment=Qt.AlignmentFlag.AlignRight)

        layout.addLayout(row1_layout)

        # 2) Row: product image, name, price, items
        row2_layout = QHBoxLayout()
        image_label = QLabel()
        pixmap = QPixmap("resources/images/smoked_burger.png")  # Placeholder
        if not pixmap.isNull():
            pixmap = pixmap.scaled(60, 60, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            image_label.setPixmap(pixmap)
        else:
            image_label.setText("No Image")
        image_label.setFixedSize(60, 60)
        row2_layout.addWidget(image_label)

        info_layout = QVBoxLayout()
        info_layout.setSpacing(4)

        product_name_label = QLabel("Burger With Meat")
        product_name_label.setFont(QFont(SETTINGS["font_family"], 14, QFont.Weight.Bold))
        product_name_label.setStyleSheet("color: #1E1E1E;")
        info_layout.addWidget(product_name_label)

        price_label = QLabel("€12")
        price_label.setFont(QFont(SETTINGS["font_family"], 12))
        price_label.setStyleSheet("color: #FE8C00;")
        info_layout.addWidget(price_label)

        row2_layout.addLayout(info_layout)
        row2_layout.addStretch()

        items_label = QLabel("14 items")
        items_label.setFont(QFont(SETTINGS["font_family"], 12))
        items_label.setStyleSheet("color: #9A9A9A;")
        row2_layout.addWidget(items_label, alignment=Qt.AlignmentFlag.AlignRight)

        layout.addLayout(row2_layout)

        return card_container

    def create_profile_options(self) -> QWidget:
        """
        Creates the list of profile options:
         - Personal Data
         - Settings
         - Extra Card
         - Help Center
         - Request Account Deletion
         - Add another account
        """
        logging.debug("Creating profile options list.")
        container = QFrame()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(16, 8, 16, 8)
        container_layout.setSpacing(8)

        options_data = [
            ("Personal Data", "resources/icons/user.png"),
            ("Settings", "resources/icons/settings.png"),
            ("Extra Card", "resources/icons/card.png"),
            ("Help Center", "resources/icons/help.png"),
            ("Request Account Deletion", "resources/icons/delete.png"),
            ("Add another account", "resources/icons/add_user.png"),
        ]

        for label_text, icon_path in options_data:
            option_btn = self.create_option_row(label_text, icon_path)
            container_layout.addWidget(option_btn)

        return container

    def create_option_row(self, text: str, icon_path: str) -> QWidget:
        """
        Creates a horizontal row with an icon, text, and a '>' arrow on the right.
        """
        row_frame = QFrame()
        row_layout = QHBoxLayout(row_frame)
        row_layout.setContentsMargins(0, 0, 0, 0)
        row_layout.setSpacing(8)

        icon_label = QLabel()
        pixmap = QPixmap(icon_path)
        if not pixmap.isNull():
            pixmap = pixmap.scaled(24, 24, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            icon_label.setPixmap(pixmap)
        else:
            icon_label.setText("No Icon")
        icon_label.setFixedSize(24, 24)
        row_layout.addWidget(icon_label)

        text_label = QLabel(text)
        text_label.setFont(QFont(SETTINGS["font_family"], 12))
        text_label.setStyleSheet("color: #1E1E1E;")
        row_layout.addWidget(text_label, stretch=1)

        # Right arrow
        arrow_label = QLabel()
        arrow_pix = QPixmap("resources/icons/arrow_right.png")
        if not arrow_pix.isNull():
            arrow_pix = arrow_pix.scaled(20, 20, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            arrow_label.setPixmap(arrow_pix)
        else:
            arrow_label.setText(">")
        arrow_label.setFixedSize(20, 20)
        row_layout.addWidget(arrow_label, alignment=Qt.AlignmentFlag.AlignRight)

        return row_frame

    def create_sign_out_button(self) -> QWidget:
        """
        Creates a sign out button in red.
        """
        logging.debug("Creating sign out button.")
        container = QFrame()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(16, 16, 16, 16)
        container_layout.setSpacing(0)

        btn_sign_out = QPushButton("Sign Out")
        btn_sign_out.setFont(QFont(SETTINGS["font_family"], 14, QFont.Weight.Bold))
        btn_sign_out.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #FA3E3E;
                border: 1px solid #FA3E3E;
                border-radius: 8px;
                padding: 12px;
            }
            QPushButton:hover {
                background-color: #FA3E3E;
                color: white;
            }
        """)
        # Connect as needed: btn_sign_out.clicked.connect(...)
        container_layout.addWidget(btn_sign_out)

        return container
