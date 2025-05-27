# view/add_card_dialog.py

import os
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QComboBox,
    QFrame,
)
from PyQt6.QtGui import QPixmap, QFont, QIcon
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from config.settings import SETTINGS


class AddCardDialog(QDialog):
    saved = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Card")
        self.setModal(True)
        self.setup_ui()

    def setup_ui(self):
        base = os.path.dirname(os.path.abspath(__file__))

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)

        # ─── Card Preview Image at Top ───────────────────────────
        card_label = QLabel()
        card_pix = QPixmap(
            os.path.join(base, "..", "resources", "images", "Bank_Account.png")
        )
        card_label.setPixmap(
            card_pix.scaledToHeight(200, Qt.TransformationMode.SmoothTransformation)
        )
        card_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(card_label)

        # ─── Form Fields ──────────────────────────────────────────

        def labeled_input(label_text, default=""):
            fr = QFrame()
            v = QVBoxLayout(fr)
            lbl = QLabel(label_text)
            lbl.setFont(QFont(SETTINGS["font_family"], 12))
            inp = QLineEdit(default)
            inp.setFixedHeight(40)
            inp.setStyleSheet(
                f"""
                QLineEdit{{
                    border:1px solid {SETTINGS["colors"]["neutral"]["Neutral 30"]};
                    border-radius:8px;
                    padding:0 8px; 
                }}
            """
            )
            v.addWidget(lbl)
            v.addWidget(inp)
            return fr, inp

        # Cardholder Name
        name_frame, self.name_edit = labeled_input("Cardholder Name", "")
        name_frame.setStyleSheet(
            f"color: {SETTINGS["colors"]["neutral"]["Neutral 100"]};"
        )
        layout.addWidget(name_frame)

        # Card Number with icon on right
        num_frame = QFrame()
        num_frame.setStyleSheet(
            f"color: {SETTINGS["colors"]["neutral"]["Neutral 100"]};"
        )
        num_layout = QHBoxLayout(num_frame)
        num_layout.setContentsMargins(0, 0, 0, 0)
        num_layout.setSpacing(0)
        lbl_num = QLabel("Card Number")
        lbl_num.setFont(QFont(SETTINGS["font_family"], 12))
        num_layout.addWidget(lbl_num, alignment=Qt.AlignmentFlag.AlignLeft)
        num_layout.addStretch()
        layout.addWidget(num_frame)

        num_inp = QLineEdit("3822 8293 8292 2356")
        num_inp.setFixedHeight(40)
        num_inp.setStyleSheet(
            f"""
                QLineEdit{{
                    color: {SETTINGS["colors"]["neutral"]["Neutral 100"]};
                    border:1px solid {SETTINGS["colors"]["neutral"]["Neutral 30"]};
                    border-radius:8px;
                    padding:0 8px; 
                }}
            """
        )
        # embed icon on the right:
        icon = QIcon(os.path.join(base, "..", "resources", "icons", "bank.png"))
        num_inp.addAction(icon, QLineEdit.ActionPosition.TrailingPosition)
        self.number_edit = num_inp
        layout.addWidget(num_inp)

        # Expiry + CVV side by side
        row = QHBoxLayout()
        # Expiry
        exp_frame, self.expiry_edit = labeled_input("Expiry Date", "")
        exp_frame.setStyleSheet(
            f"color: {SETTINGS["colors"]["neutral"]["Neutral 100"]};"
        )
        row.addWidget(exp_frame)
        # CVV
        cvv_frame, self.cvv_edit = labeled_input("3-Digit CVV", "")
        cvv_frame.setStyleSheet(
            f"color: {SETTINGS["colors"]["neutral"]["Neutral 100"]};"
        )
        row.addWidget(cvv_frame)
        layout.addLayout(row)

        # ─── Save Button ────────────────────────────────────────────
        save = QPushButton("Save Card")
        save.setFixedHeight(50)
        save.setFont(QFont(SETTINGS["font_family"], 14, QFont.Weight.Bold))
        save.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {SETTINGS["colors"]["primary"]["hover"]};
                color: white;
                border-radius: 25px;
            }}
            QPushButton:pressed {{
                background-color: #e07f00;
            }}
        """
        )
        save.clicked.connect(self.on_save)
        layout.addWidget(save)

    def on_save(self):
        data = {
            "holder": self.name_edit.text(),
            "number": self.number_edit.text(),
            "expiry": self.expiry_edit.text(),
            "cvv": self.cvv_edit.text(),
        }
        self.saved.emit(data)
        self.accept()
