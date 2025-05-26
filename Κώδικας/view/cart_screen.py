import logging
import os

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, QPushButton,
    QFrame, QScrollArea, QCheckBox, QToolButton, QSpinBox, QSizePolicy
)
from PyQt6.QtGui import QFont, QIcon, QPixmap
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from config.settings import SETTINGS
from view.components.bottom_nav import BottomNav

class CartScreen(QWidget):
    """
    A Cart Screen closely replicating the provided design.
    Includes a top bar, delivery location info, promo code row,
    cart items, payment summary, and an 'Order Now' button.
    """
    backClicked = pyqtSignal()  # Emitted when the back button is pressed

    def __init__(self, parent=None):
        super().__init__(parent)
        logging.debug("Initializing CartScreen.")
        self.setup_ui()

    def setup_ui(self):
        """
        Build the UI using layouts and placeholder data.
        """
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Create a scroll area so the cart can handle multiple items
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        # Content widget inside the scroll area
        content_widget = QFrame()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        # 1. Top Bar: "My Cart"
        top_bar = self.create_top_bar()
        content_layout.addWidget(top_bar)

        # 2. Delivery Location Row
        delivery_row = self.create_delivery_row()
        content_layout.addWidget(delivery_row)

        # 3. Promo Code Row
        promo_row = self.create_promo_row()
        content_layout.addWidget(promo_row)

        # 4. Cart Items Section (2 placeholders for now)
        cart_items_section = self.create_cart_items_section()
        content_layout.addWidget(cart_items_section)

        # 5. Payment Summary
        payment_summary = self.create_payment_summary()
        content_layout.addWidget(payment_summary)

        # Add stretch so the "Order Now" button stays at bottom
        content_layout.addStretch()

        # 6. "Order Now" button
        order_button = self.create_order_button()
        content_layout.addWidget(order_button)

        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)

        # ----- Bottom Navigation (Fixed) -----
        # Create the BottomNav widget with a fixed height and a non-transparent background.
        self.bottom_nav = BottomNav(current_tab="cart", parent=self)
        self.bottom_nav.setFixedHeight(70)
        # Update its stylesheet to have a solid background color. You can refer to your settings.
        self.bottom_nav.setStyleSheet(f"background-color: {SETTINGS['colors']['neutral']['Neutral 10']};")
        # Add the bottom nav at the bottom of the main layout.

        main_layout.addWidget(self.bottom_nav)

        self.setLayout(main_layout)
        logging.debug("CartScreen UI setup completed.")

    # ----------------------------------------------------------------
    #   UI Section Constructors
    # ----------------------------------------------------------------

    def create_top_bar(self) -> QWidget:
        """
        Creates a top bar with the screen title "My Cart."
        """
        logging.debug("Creating top bar for CartScreen.")
        container = QFrame()
        container.setFixedHeight(56)
        container.setStyleSheet("background: transparent;")
        layout = QHBoxLayout(container)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)

        # Back Button.
        btn_back = QToolButton()
        btn_back.setIcon(QIcon("resources/icons/Back2.png"))
        btn_back.setIconSize(QSize(40, 40))
        btn_back.setStyleSheet("border: none;")
        btn_back.clicked.connect(self.on_back_clicked)
        layout.addWidget(btn_back, alignment=Qt.AlignmentFlag.AlignLeft)

        # Title label (centered).
        title_label = QLabel("My Cart")
        title_label.setFont(QFont(SETTINGS["font_family"], 14, QFont.Weight.Bold))
        title_label.setStyleSheet(f"color: {SETTINGS['colors']['neutral']['Neutral 100']};")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label, stretch=1)

        # Favorite / Share Button.
        btn_favorite = QToolButton()
        btn_favorite.setIcon(QIcon("resources/icons/bots.png"))
        btn_favorite.setIconSize(QSize(40, 40))
        btn_favorite.setStyleSheet("border: none;")
        layout.addWidget(btn_favorite, alignment=Qt.AlignmentFlag.AlignRight)

        return container

    def on_back_clicked(self):
        logging.debug("Back button clicked in Cart.")
        self.backClicked.emit()

    def create_delivery_row(self) -> QWidget:
        """
        Creates the 'Delivery Location' row with 'Home' and a 'Change Location' button.
        """
        logging.debug("Creating delivery row.")
        container = QFrame()
        container.setFixedHeight(50)
        layout = QHBoxLayout(container)
        layout.setContentsMargins(16, 0, 16, 0)
        layout.setSpacing(0)

        # Left side: "Delivery Location" + "Home"
        left_col = QVBoxLayout()
        left_col.setSpacing(0)

        lbl_location_title = QLabel("Delivery Location")
        lbl_location_title.setFont(QFont(SETTINGS["font_family"], 12, QFont.Weight.Normal))
        lbl_location_title.setStyleSheet("color: #9A9A9A;")
        left_col.addWidget(lbl_location_title)

        lbl_current_location = QLabel("Home")
        lbl_current_location.setFont(QFont(SETTINGS["font_family"], 12, QFont.Weight.Bold))
        lbl_current_location.setStyleSheet("color: #1E1E1E;")
        left_col.addWidget(lbl_current_location)

        layout.addLayout(left_col)
        layout.addStretch()

        # Right side: "Change Location" button
        btn_change_location = QPushButton("Change Location")
        btn_change_location.setFont(QFont(SETTINGS["font_family"], 10))
        btn_change_location.setStyleSheet("""
            QPushButton {
                color: #FE8C00; 
                border: 1px solid #FE8C00;
                border-radius: 20px;
                padding: 12px 30px;
                background: transparent;
            }
            QPushButton:hover {
                text-decoration: underline;
            }
        """)
        # Connect a slot if needed: btn_change_location.clicked.connect(...)
        layout.addWidget(btn_change_location, alignment=Qt.AlignmentFlag.AlignRight)

        return container

    def create_promo_row(self) -> QWidget:
        """
        Creates the row for Promo Code input and an 'Apply' button.
        """
        logging.debug("Creating promo code row.")
        container = QFrame()
        container.setFixedHeight(50)
        layout = QHBoxLayout(container)
        layout.setContentsMargins(16, 0, 16, 0)
        layout.setSpacing(8)

        # Promo Code Input
        promo_input = QLineEdit()
        promo_input.setPlaceholderText("Promo Code. . .")
        promo_input.setFont(QFont(SETTINGS["font_family"], 12))
        promo_input.setStyleSheet("""
            QLineEdit {
                color: black;
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                padding: 4px 8px;
            }
        """)
        layout.addWidget(promo_input)

        # Apply Button
        btn_apply = QPushButton("Apply")
        btn_apply.setFont(QFont(SETTINGS["font_family"], 10))
        btn_apply.setStyleSheet("""
            QPushButton {
                background-color: #FE8C00;
                color: white;
                border-radius: 12px;
                padding: 4px 16px;
            }
            QPushButton:hover {
                background-color: #FF9E22;
            }
        """)
        layout.addWidget(btn_apply, alignment=Qt.AlignmentFlag.AlignRight)

        return container

    def create_cart_items_section(self) -> QWidget:
        """
        Creates a section with cart items, each item displaying:
         - A checkbox to select
         - An image
         - The item name & price
         - A quantity control
         - A remove/trash button
        """
        logging.debug("Creating cart items section.")
        container = QFrame()
        container.setObjectName("cartItemsSection")
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(16, 8, 16, 8)
        container_layout.setSpacing(16)

        # Add two placeholder items
        item1 = self.create_cart_item_widget(
            image="resources/images/smoked_burger.png",
            name="Burger With Meat",
            price="€ 12"
        )
        item2 = self.create_cart_item_widget(
            image="resources/images/classic_burger.png",
            name="Ordinary Burgers",
            price="€ 12"
        )

        container_layout.addWidget(item1)
        container_layout.addWidget(item2)

        return container

    def create_cart_item_widget(self, image: str, name: str, price: str) -> QWidget:
        """
        Creates an individual cart item row.
        """
        item_container = QFrame()
        item_container.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border-radius: 12px;
            }
        """)
        layout = QHBoxLayout(item_container)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)

        # 1) Checkbox
        # checkbox = QCheckBox()
        # checkbox.setChecked(True)  # Placeholder default
        # layout.addWidget(checkbox, alignment=Qt.AlignmentFlag.AlignTop)

        # 2) Product Image
        img_label = QLabel()
        pixmap = QPixmap(image)
        if not pixmap.isNull():
            pixmap = pixmap.scaled(60, 60, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            img_label.setPixmap(pixmap)
        else:
            img_label.setText("No Image")
        img_label.setFixedSize(60, 60)
        layout.addWidget(img_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # 3) Product Name & Price + quantity
        info_layout = QVBoxLayout()
        info_layout.setSpacing(4)

        name_label = QLabel(name)
        name_label.setFont(QFont(SETTINGS["font_family"], 14, QFont.Weight.Bold))
        name_label.setStyleSheet("color: #1E1E1E;")
        info_layout.addWidget(name_label)

        price_label = QLabel(price)
        price_label.setFont(QFont(SETTINGS["font_family"], 12, QFont.Weight.Bold))
        price_label.setStyleSheet("color: #FE8C00;")
        info_layout.addWidget(price_label)

        # Quantity controls (minus, spinbox, plus) or
        # or just a spinbox in a horizontal layout
        qty_layout = QHBoxLayout()


        quantity_spinbox = QSpinBox()
        quantity_spinbox.setRange(1, 99)
        quantity_spinbox.setValue(1)
        quantity_spinbox.setStyleSheet("""
            QSpinBox {
                width: 40px;
                border: 1px solid #E0E0E0;
                border-radius: 4px;
                color: black;
            }
        """)
        qty_layout.addWidget(quantity_spinbox)


        info_layout.addLayout(qty_layout)

        layout.addLayout(info_layout)

        # 4) Remove / trash button (far right)
        remove_btn = QToolButton()
        remove_btn.setIcon(QIcon("resources/icons/trash.png"))
        remove_btn.setIconSize(QSize(20, 20))
        remove_btn.setStyleSheet("border: none; background-color: transparent;")
        # remove_btn.clicked.connect(...) # If you want to handle removal
        layout.addWidget(remove_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        return item_container

    def create_payment_summary(self) -> QWidget:
        """
        Creates the Payment Summary block with placeholders:
          - Total Items (3)
          - Delivery Fee (Free)
          - Discount
          - Total
        """
        logging.debug("Creating payment summary section.")
        container = QFrame()
        container.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border-radius: 12px;
            }
        """)
        layout = QVBoxLayout(container)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(8)

        # Title label
        title_label = QLabel("Payment Summary")
        title_label.setFont(QFont(SETTINGS["font_family"], 14, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #1E1E1E;")
        layout.addWidget(title_label)

        # Items
        lbl_items = QLabel("Total Items (3)")
        lbl_items.setFont(QFont(SETTINGS["font_family"], 12))
        lbl_items.setStyleSheet("color: #646464;")
        layout.addWidget(lbl_items)

        lbl_delivery_fee = QLabel("Delivery Fee   Free")
        lbl_delivery_fee.setFont(QFont(SETTINGS["font_family"], 12))
        lbl_delivery_fee.setStyleSheet("color: #646464;")
        layout.addWidget(lbl_delivery_fee)

        lbl_discount = QLabel("Discount   -")
        lbl_discount.setFont(QFont(SETTINGS["font_family"], 12))
        lbl_discount.setStyleSheet("color: #646464;")
        layout.addWidget(lbl_discount)

        # Divider
        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(divider)

        lbl_total = QLabel("Total   €12")
        lbl_total.setFont(QFont(SETTINGS["font_family"], 14, QFont.Weight.Bold))
        lbl_total.setStyleSheet("color: #1E1E1E;")
        layout.addWidget(lbl_total)

        return container

    def create_order_button(self) -> QWidget:
        """
        Creates the 'Order Now' button at the bottom.
        """
        logging.debug("Creating 'Order Now' button.")
        container = QFrame()
        container.setFixedHeight(80)
        container.setStyleSheet("background-color: transparent;")
        layout = QHBoxLayout(container)
        layout.setContentsMargins(16, 0, 16, 0)
        layout.setSpacing(0)

        btn_order = QPushButton("Order Now")
        btn_order.setFont(QFont(SETTINGS["font_family"], 14, QFont.Weight.Bold))
        btn_order.setStyleSheet("""
            QPushButton {
                background-color: #FE8C00;
                color: white;
                border-radius: 10px;
                padding: 12px;
            }
            QPushButton:hover {
                background-color: #FF9E22;
            }
        """)
        btn_order.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        # btn_order.clicked.connect(...) # If you want to handle placing the order
        layout.addWidget(btn_order)

        return container
