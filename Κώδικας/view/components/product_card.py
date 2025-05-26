# view/components/product_card.py
import os
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt, pyqtSignal


class ProductCard(QFrame):
    # Emit this signal when the card is clicked.
    clicked = pyqtSignal()

    def __init__(self, image, title, rating, distance, price):
        super().__init__()

        self.setFixedSize(160, 240)
        self.setStyleSheet(
            """
            QFrame {
                background-color: white;
                border-radius: 16px;
            }
        """
        )

        layout = QVBoxLayout()
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)

        # --- Product Image ---
        image_label = QLabel()
        pixmap = QPixmap(image).scaled(
            144,
            100,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(image_label)

        # --- Title ---
        title_label = QLabel(title)
        title_label.setFont(QFont("Inter", 12, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #1E1E1E;")
        layout.addWidget(title_label)

        # --- Rating and Distance Row (with icons) ---
        info_layout = QHBoxLayout()
        info_layout.setSpacing(4)
        # Compute the base directory relative to this file.
        script_dir = os.path.dirname(os.path.abspath(__file__))
        star_icon_path = os.path.join(
            script_dir, "..", "..", "resources", "icons", "star.png"
        )
        location_icon_path = os.path.join(
            script_dir, "..", "..", "resources", "icons", "location.png"
        )
        print(f"DEBUG: Star icon path: {star_icon_path}")
        print(f"DEBUG: Location icon path: {location_icon_path}")
        # Star icon for rating
        star_label = QLabel()
        star_pix = QPixmap(star_icon_path).scaled(
            14,
            14,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        star_label.setPixmap(star_pix)
        info_layout.addWidget(star_label)

        # Rating text
        rating_label = QLabel(rating)
        rating_label.setStyleSheet("color: #9A9A9A; font-size: 11px;")
        info_layout.addWidget(rating_label)

        # Separator bullet
        bullet_label = QLabel("    ")
        bullet_label.setStyleSheet("color: #9A9A9A; font-size: 11px;")
        info_layout.addWidget(bullet_label)

        # Location icon for distance
        location_icon_label = QLabel()
        loc_pix = QPixmap(location_icon_path).scaled(
            14,
            14,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        location_icon_label.setPixmap(loc_pix)
        info_layout.addWidget(location_icon_label)

        # Distance text
        distance_label = QLabel(distance)
        distance_label.setStyleSheet("color: #9A9A9A; font-size: 11px;")
        info_layout.addWidget(distance_label)

        layout.addLayout(info_layout)

        # --- Price Row ---
        bottom_row = QHBoxLayout()
        price_label = QLabel(price)
        price_label.setFont(QFont("Inter", 12, QFont.Weight.Bold))
        price_label.setStyleSheet("color: #FE8C00;")
        bottom_row.addWidget(price_label)
        bottom_row.addStretch()
        layout.addLayout(bottom_row)

        self.setLayout(layout)

    def mousePressEvent(self, event):
        print("DEBUG: ProductCard clicked!")
        self.clicked.emit()
        event.accept()  # Accept the event without calling super().
