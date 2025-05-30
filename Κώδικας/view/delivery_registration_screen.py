import os
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QComboBox,
    QScrollArea,
    QFrame,
    QMessageBox,
)
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from config.settings import SETTINGS


class DeliveryRegistrationScreen(QWidget):
    backClicked = pyqtSignal()
    registerClicked = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet("background-color: white;")
        main = QVBoxLayout(self)
        main.setContentsMargins(16, 16, 16, 16)
        main.setSpacing(16)

        # ─── Header ───────────────────────────────────────────────────────────
        header = QHBoxLayout()
        back_btn = QPushButton()
        back_btn.setIcon(QIcon(os.path.join("resources", "icons", "arrow_back.png")))
        back_btn.setIconSize(QSize(24, 24))
        back_btn.setFixedSize(36, 36)
        back_btn.setStyleSheet("border: none; background-color: transparent;")
        back_btn.clicked.connect(lambda: self.backClicked.emit())

        title = QLabel("Delivery Registration")
        title.setFont(QFont(SETTINGS["font_family"], 16, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {SETTINGS['colors']['neutral']['Neutral 100']};")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        header.addWidget(back_btn)
        header.addStretch()
        header.addWidget(title)
        header.addStretch()
        header.addSpacing(36)
        main.addLayout(header)

        # ─── Scrollable Form ─────────────────────────────────────────────────
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        form_container = QWidget()
        form = QVBoxLayout(form_container)
        form.setSpacing(12)

        # helper to build labelled input
        def labeled_input(label_text, placeholder=""):
            wrapper = QFrame()
            v = QVBoxLayout(wrapper)
            lbl = QLabel(label_text)
            lbl.setFont(QFont(SETTINGS["font_family"], 12))
            lbl.setStyleSheet(f"color: {SETTINGS['colors']['neutral']['Neutral 100']};")
            inp = QLineEdit()
            inp.setPlaceholderText(placeholder)
            inp.setFixedHeight(40)
            inp.setStyleSheet(
                f"""
                QLineEdit {{
                    border: 1px solid {SETTINGS['colors']['neutral']['Neutral 30']};
                    border-radius: 8px;
                    padding-left: 8px;
                    color: {SETTINGS['colors']['neutral']['Neutral 100']};
                }}
            """
            )
            v.addWidget(lbl)
            v.addWidget(inp)
            return wrapper, inp

        # Full Name
        frame_name, self.name_edit = labeled_input("Full Name", "e.g. John Doe")
        form.addWidget(frame_name)

        # Email
        frame_email, self.email_edit = labeled_input("Email", "you@example.com")
        form.addWidget(frame_email)

        # Phone
        frame_phone, self.phone_edit = labeled_input("Phone Number", "+30 69x xxx xxxx")
        form.addWidget(frame_phone)

        # Vehicle Type
        vehicle_frame = QFrame()
        vv = QVBoxLayout(vehicle_frame)
        lbl_vehicle = QLabel("Vehicle Type")
        lbl_vehicle.setFont(QFont(SETTINGS["font_family"], 12))
        lbl_vehicle.setStyleSheet(
            f"color: {SETTINGS['colors']['neutral']['Neutral 100']};"
        )
        combo_vehicle = QComboBox()
        combo_vehicle.addItems(["Motorbike", "Car", "Bicycle", "Van"])
        combo_vehicle.setFixedHeight(40)
        combo_vehicle.setStyleSheet(
            f"""
            QComboBox {{
                border: 1px solid {SETTINGS['colors']['neutral']['Neutral 30']};
                border-radius: 8px;
                padding-left: 8px;
                color: {SETTINGS['colors']['neutral']['Neutral 100']};
            }}
        """
        )
        vv.addWidget(lbl_vehicle)
        vv.addWidget(combo_vehicle)
        self.vehicle_combo = combo_vehicle
        form.addWidget(vehicle_frame)

        # License Plate
        frame_plate, self.plate_edit = labeled_input("License Plate", "ABC-1234")
        form.addWidget(frame_plate)

        # Password
        frame_pw, self.pw_edit = labeled_input("Password", "")
        self.pw_edit.setEchoMode(QLineEdit.EchoMode.Password)
        form.addWidget(frame_pw)

        # Confirm Password
        frame_pw2, self.pw2_edit = labeled_input("Confirm Password", "")
        self.pw2_edit.setEchoMode(QLineEdit.EchoMode.Password)
        form.addWidget(frame_pw2)

        form.addStretch()
        scroll.setWidget(form_container)
        main.addWidget(scroll)

        # ─── Register Button ─────────────────────────────────────────────────
        register_btn = QPushButton("Register")
        register_btn.setFixedHeight(50)
        register_btn.setFont(QFont(SETTINGS["font_family"], 14, QFont.Weight.Bold))
        register_btn.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {SETTINGS['colors']['primary']['hover']};
                color: white;
                border-radius: 25px;
            }}
            QPushButton:pressed {{
                background-color: {SETTINGS['colors']['primary']['hover']};
            }}
        """
        )
        register_btn.clicked.connect(self.on_register)
        main.addWidget(register_btn)

    def on_register(self):
        # simple validation
        if not self.name_edit.text().strip():
            QMessageBox.warning(self, "Validation", "Full Name is required")
            return
        if self.pw_edit.text() != self.pw2_edit.text():
            QMessageBox.warning(self, "Validation", "Passwords do not match")
            return

        data = {
            "name": self.name_edit.text().strip(),
            "email": self.email_edit.text().strip(),
            "phone": self.phone_edit.text().strip(),
            "vehicle": self.vehicle_combo.currentText(),
            "license_plate": self.plate_edit.text().strip(),
            "password": self.pw_edit.text(),
        }
        self.registerClicked.emit(data)
