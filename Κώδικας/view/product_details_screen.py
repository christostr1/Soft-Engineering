import os
import logging

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea,
    QFrame, QHBoxLayout, QToolButton, QSpinBox, QSizePolicy, QGridLayout
)
from PyQt6.QtGui import QPixmap, QFont, QIcon
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from config.settings import SETTINGS
from view.components.product_card import ProductCard  # Ensure this component is available


class ProductDetailsScreen(QWidget):
    """
    A screen that displays detailed information about a product.
    It includes:
      - A top overlay bar (with a back button) placed on top of the product image.
      - The product image.
      - A header divided into two parts:
          • A row for Price.
          • A row for Delivery info, Estimated Time, and Rating (each with an icon).
      - Product title and description.
      - A horizontal "Recommended For You" section showing ProductCards.
      - A bottom bar with quantity controls and an Add to Cart button.
    """
    # Signal for the back button so the main application can navigate back.
    backClicked = pyqtSignal()

    def __init__(self, product_data: dict, parent=None):
        """
        :param product_data: Expected keys:
            'image'        - Path to product image.
            'price'        - Price string (e.g. "€12").
            'delivery'     - Delivery cost or label (e.g. "Free Delivery").
            'time'         - Estimated time (e.g. "20-30").
            'rating'       - Rating (e.g. "4.5").
            'title'        - Product title/name (e.g. "Burger With Meat 🍔").
            'description'  - Product description.
        """
        super().__init__(parent)
        self.product_data = product_data
        logging.debug("Initializing ProductDetailsScreen with product_data: %s", self.product_data)
        self.setup_ui()

    def setup_ui(self):
        """Sets up the entire UI for the Product Details screen."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Create a scroll area to wrap all content.
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        # Content widget holds the scrollable content.
        content_widget = QFrame()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        # --- 1. Image Container (Product Image with Top Bar Overlay) ---
        image_container = self.create_image_container()
        content_layout.addWidget(image_container)

        # --- 2. Product Title ---
        title_label = self.create_title_label()
        content_layout.addWidget(title_label)

        # --- 3. Price Row ---
        price_row = self.create_price_row()
        content_layout.addLayout(price_row)

        # --- 4. Info Row (Delivery, Time, Rating with Icons) ---
        info_row = self.create_info_row()
        content_layout.addLayout(info_row)

        # --- 5. Description Section ---
        desc_section = self.create_description_section()
        content_layout.addWidget(desc_section)

        # --- 6. Recommended For You Section ---
        recommended_section = self.create_recommended_section()
        content_layout.addWidget(recommended_section)

        # Add stretch to push content upward in case of extra space.
        content_layout.addStretch()

        # --- 7. Bottom Bar (Quantity + Add to Cart) ---
        bottom_bar = self.create_bottom_bar()
        content_layout.addWidget(bottom_bar)

        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)

        self.setLayout(main_layout)
        logging.debug("ProductDetailsScreen UI setup completed.")

    def create_image_container(self) -> QWidget:
        """
        Creates a container that holds the product image and overlays the top bar on it.
        """
        logging.debug("Creating image container with product image and top bar overlay.")
        container = QFrame()
        container.setFixedHeight(220)
        container.setFixedWidth(398)
        container.setStyleSheet(f"background-color: #000000;")

        # Use absolute positioning in the container.
        container.setLayout(QVBoxLayout())
        container.layout().setContentsMargins(0, 0, 0, 0)

        # Product Image Label.
        image_label = QLabel(container)
        image_label.setFixedSize(container.size())
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image_path = self.product_data.get("image", "")
        if os.path.isfile(image_path):
            pixmap = QPixmap(image_path)
            # Scale the image to fill container while keeping aspect ratio.
            pixmap = pixmap.scaled(398, image_label.height(),
                                   Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                                   Qt.TransformationMode.SmoothTransformation)
            image_label.setPixmap(pixmap)
        else:
            image_label.setText("No Image Found")
        image_label.setStyleSheet("background-color: #F7F7F7;")
        image_label.setObjectName("productImage")
        # image_label.setGeometry(0, 0, container.width(), container.height())
        image_label.show()

        # Create Top Bar and overlay it on the image.
        top_bar = self.create_top_bar()
        # Set top bar's parent to the container so it overlays.
        top_bar.setParent(container)
        # Position the top bar at the top: full width, fixed height (e.g., 56px).
        top_bar.setGeometry(0, 0, container.width(), 56)
        top_bar.raise_()
        top_bar.show()

        return container

    def create_top_bar(self) -> QWidget:
        """
        Creates the top bar overlay with a back button and a title.
        """
        logging.debug("Creating top bar overlay.")
        container = QFrame()
        container.setFixedHeight(56)
        container.setStyleSheet("background: transparent;")
        layout = QHBoxLayout(container)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)

        # Back Button.
        btn_back = QToolButton()
        btn_back.setIcon(QIcon("resources/icons/arrow_back.png"))
        btn_back.setIconSize(QSize(40, 40))
        btn_back.setStyleSheet("border: none;")
        btn_back.clicked.connect(self.on_back_clicked)
        layout.addWidget(btn_back, alignment=Qt.AlignmentFlag.AlignLeft)

        # Title label (centered).
        title_label = QLabel("About This Menu")
        title_label.setFont(QFont(SETTINGS["font_family"], 14, QFont.Weight.Bold))
        title_label.setStyleSheet(f"color: {SETTINGS['colors']['neutral']['Neutral 10']};")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label, stretch=1)

        # Favorite / Share Button.
        btn_favorite = QToolButton()
        btn_favorite.setIcon(QIcon("resources/icons/favorite.png"))
        btn_favorite.setIconSize(QSize(40, 40))
        btn_favorite.setStyleSheet("border: none;")
        layout.addWidget(btn_favorite, alignment=Qt.AlignmentFlag.AlignRight)

        return container

    def on_back_clicked(self):
        logging.debug("Back button clicked in ProductDetailsScreen.")
        self.backClicked.emit()

    def create_price_row(self) -> QHBoxLayout:
        """
        Creates a row displaying just the product price.
        """
        logging.debug("Creating price row.")
        layout = QHBoxLayout()
        layout.setContentsMargins(16, 16, 16, 0)
        # Retrieve price from product data.
        price = self.product_data.get("price", "€0")
        lbl_price = QLabel(price)
        lbl_price.setFont(QFont(SETTINGS["font_family"], 14, QFont.Weight.Bold))
        # Use a color from your config (for example, using a neutral value)
        lbl_price.setStyleSheet(f"color: {SETTINGS['colors']['primary']['hover']};")
        layout.addWidget(lbl_price)
        layout.addStretch()
        return layout

    def create_info_row(self) -> QHBoxLayout:
        """
        Creates a row displaying Delivery, Time, and Rating information.
        Each piece is preceded by an icon.
        """
        logging.debug("Creating info row (delivery, time, rating with icons).")
        layout = QHBoxLayout()
        layout.setContentsMargins(16, 16, 16, 0)
        layout.setSpacing(70)

        # Delivery Section.
        delivery = self.product_data.get("delivery", "Free Delivery")
        delivery_widget = self.create_info_item("resources/icons/delivery.png", delivery)
        layout.addWidget(delivery_widget)

        # Time Section.
        time_range = self.product_data.get("time", "20-30")
        time_widget = self.create_info_item("resources/icons/clock.png", time_range)
        layout.addWidget(time_widget)

        # Rating Section.
        rating = self.product_data.get("rating", "N/A")
        rating_widget = self.create_info_item("resources/icons/star.png", rating)
        layout.addWidget(rating_widget)

        layout.addStretch()
        return layout

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
        pixmap = pixmap.scaled(16, 16, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        icon_label.setPixmap(pixmap)
        icon_label.setFixedSize(16, 16)
        item_layout.addWidget(icon_label)

        text_label = QLabel(text)
        text_label.setFont(QFont(SETTINGS["font_family"], 12))
        text_label.setStyleSheet("color: #646464;")
        item_layout.addWidget(text_label)

        return container

    def create_title_label(self) -> QLabel:
        """
        Displays the product's main title, e.g., "Burger With Meat 🍔"
        """
        logging.debug("Creating product title label.")
        product_title = self.product_data.get("title", "No Title")
        lbl_title = QLabel(product_title)
        lbl_title.setFont(QFont(SETTINGS["font_family"], 24, QFont.Weight.Bold))
        lbl_title.setStyleSheet(f"color: {SETTINGS["colors"]["neutral"]["Neutral 100"]};")
        lbl_title.setContentsMargins(16, 8, 16, 0)
        return lbl_title

    def create_description_section(self) -> QWidget:
        """
        Creates a section containing the product description.
        """
        logging.debug("Creating product description section.")
        container = QFrame()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(16, 8, 16, 0)
        layout.setSpacing(8)

        # Section title.
        lbl_subtitle = QLabel("Description")
        lbl_subtitle.setFont(QFont(SETTINGS["font_family"], 12, QFont.Weight.Bold))
        lbl_subtitle.setStyleSheet(f"color: {SETTINGS['colors']['neutral']['Neutral 100']};")
        layout.addWidget(lbl_subtitle)

        # Actual description.
        description_text = self.product_data.get("description",
                                                 "Burger With Meat is a popular dish, known for its rich flavors and high-quality ingredients. It is highly recommended.")
        lbl_description = QLabel(description_text)
        lbl_description.setFont(QFont(SETTINGS["font_family"], 12))
        lbl_description.setStyleSheet(f"color: {SETTINGS['colors']['neutral']['Neutral 60']};")
        lbl_description.setWordWrap(True)
        layout.addWidget(lbl_description)

        return container

    def create_recommended_section(self) -> QWidget:
        """
        Creates the 'Recommended For You' section using ProductCard components
        in a horizontal scroll area.
        """
        logging.debug("Creating recommended section.")
        container = QFrame()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(16, 16, 16, 0)
        layout.setSpacing(8)

        # Title Row.
        title_row = QHBoxLayout()
        lbl_recommended = QLabel("Recommended For You")
        lbl_recommended.setFont(QFont(SETTINGS["font_family"], 14, QFont.Weight.Bold))
        lbl_recommended.setStyleSheet(f"color: {SETTINGS['colors']['neutral']['Neutral 100']};")
        title_row.addWidget(lbl_recommended)
        title_row.addStretch()
        btn_see_all = QPushButton("See All")
        btn_see_all.setFont(QFont(SETTINGS["font_family"], 12))
        btn_see_all.setStyleSheet(
            f"color: {SETTINGS['colors']['primary']['hover']}; border: none; background: transparent;")
        title_row.addWidget(btn_see_all)
        layout.addLayout(title_row)

        # Create a horizontal scroll area for recommended products.
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setFixedHeight(250)

        # Create a container widget that will hold the grid layout.
        rec_container = QFrame()
        rec_layout = QGridLayout()
        rec_layout.setContentsMargins(0, 0, 0, 0)
        rec_layout.setSpacing(10)

        # Hard-coded recommended product examples.
        recommended_products = [
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
                "distance": "1.5km",
                "price": "$10.00"
            },
            {
                "image": "resources/images/classic_burger.png",
                "title": "Cheese Burger",
                "rating": "4.6",
                "distance": "1.8km",
                "price": "$9.80"
            }
        ]

        # Add a ProductCard for each recommended product using enumerate.
        for i, rec_prod in enumerate(recommended_products):
            card = ProductCard(**rec_prod)
            row, col = divmod(i, 2)
            rec_layout.addWidget(card, row, col, alignment=Qt.AlignmentFlag.AlignCenter)

        # Set the grid layout in a container widget.
        rec_container.setLayout(rec_layout)
        scroll_area.setWidget(rec_container)
        layout.addWidget(scroll_area)

        logging.debug("Recommended section created successfully.")
        return container


    def create_bottom_bar(self) -> QWidget:
        """
        Creates a bottom bar with quantity controls and an 'Add to Cart' button.
        """
        logging.debug("Creating bottom bar with quantity controls and Add to Cart button.")
        container = QFrame()
        container.setFixedHeight(60)
        container.setStyleSheet(f"background-color: {SETTINGS['colors']['neutral']['Neutral 10']};")
        layout = QHBoxLayout(container)
        layout.setContentsMargins(16, 8, 16, 8)
        layout.setSpacing(8)

        # Create and style the QSpinBox (Quantity Controls)
        quantity_spinbox = QSpinBox()
        quantity_spinbox.setRange(1, 99)
        quantity_spinbox.setValue(1)
        quantity_spinbox.setStyleSheet("""
            QSpinBox {
                background-color: #FFFFFF;  /* White background */
                color: #1E1E1E;             /* Dark text color */
                border: 1px solid #CCCCCC;  /* Light gray border */
                border-radius: 5px;         /* Rounded corners */
                padding: 4px 8px;           /* Padding inside the spin box */
                font-size: 14px;            /* Font size */
            }
            QSpinBox::up-button {
                subcontrol-origin: border;
                subcontrol-position: top right;
                width: 20px;
                border-left: 1px solid #CCCCCC;
                background-color: #F0F0F0;  /* Light background for the button */
            }
            QSpinBox::down-button {
                subcontrol-origin: border;
                subcontrol-position: bottom right;
                width: 20px;
                border-left: 1px solid #CCCCCC;
                background-color: #F0F0F0;
            }
            QSpinBox::up-arrow, QSpinBox::down-arrow {
                width: 0;
                height: 0;
                border-style: solid;
                border-width: 5px;
                border-color: transparent;
            }
        """)
        layout.addWidget(quantity_spinbox)

        # 'Add to Cart' Button.
        btn_add_to_cart = QPushButton("Add to Cart")
        btn_add_to_cart.setFont(QFont(SETTINGS["font_family"], 14))
        btn_add_to_cart.setStyleSheet("""
            QPushButton {
                background-color: #FE8C00;
                color: black;
                border-radius: 10px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #FF9E22;
            }
        """)
        btn_add_to_cart.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        layout.addWidget(btn_add_to_cart)

        return container
