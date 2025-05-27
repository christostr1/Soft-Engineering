# screens/payment_methods_screen.py

import os
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QFrame,
)
from PyQt6.QtGui import QPixmap, QFont, QIcon
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from config.settings import SETTINGS

from model.payment_method import PaymentMethod


class PaymentMethodsScreen(QWidget):
    back = pyqtSignal()
    deleteClicked = pyqtSignal()
    methodSelected = pyqtSignal(str)
    addNewCard = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.selected_method = None
        self.method_frames = {}
        self.methods = [
            ("MasterCard", "**** **** 0783 7873", "mastercard.png", True),
            ("Paypal", "**** **** 0582 4672", "paypal.png", False),
            ("Apple Pay", "**** **** 0582 4672", "applepay.png", False),
        ]
        # Set initial selection
        for name, _, _, selected in self.methods:
            if selected:
                self.selected_method = name
                break
        self.setup_ui()

    def setup_ui(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))

        main = QVBoxLayout(self)
        main.setContentsMargins(16, 16, 16, 16)
        main.setSpacing(16)

        # ─── Header ───────────────────────────────────────────────────────────
        header = QHBoxLayout()
        back_btn = QPushButton()
        back_btn.setIcon(QIcon("resources/icons/Back2.png"))
        back_btn.setIconSize(QSize(40, 40))
        back_btn.setStyleSheet("border: none;")
        back_btn.clicked.connect(lambda: self.back.emit())

        title = QLabel("Extra Card")
        title.setFont(QFont(SETTINGS["font_family"], 16, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {SETTINGS['colors']['neutral']['Neutral 100']};")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        del_btn = QPushButton()
        del_btn.setIcon(QIcon("resources/icons/trash2.png"))
        del_btn.setIconSize(QSize(40, 40))
        del_btn.setStyleSheet("border: none;")
        del_btn.clicked.connect(lambda: self.deleteClicked.emit())

        header.addWidget(back_btn)
        header.addStretch()
        header.addWidget(title)
        header.addStretch()
        header.addWidget(del_btn)
        main.addLayout(header)

        # ─── Top Card Preview ─────────────────────────────────────────────────
        card_label = QLabel()
        card_pix = QPixmap(
            os.path.join(base_dir, "..", "resources", "images", "card.png")
        )
        card_label.setPixmap(card_pix)
        card_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main.addWidget(card_label)

        # ─── Saved Methods List ────────────────────────────────────────────────
        methods_layout = QVBoxLayout()
        methods_layout.setSpacing(12)
        methods_layout.setContentsMargins(0, 0, 0, 0)

        section = QLabel("Credit card")
        section.setFont(QFont(SETTINGS["font_family"], 14, QFont.Weight.Bold))
        section.setStyleSheet(f"color: {SETTINGS['colors']['neutral']['Neutral 100']};")
        methods_layout.addWidget(section)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        cont = QWidget()
        cont_l = QVBoxLayout(cont)
        cont_l.setSpacing(7)

        # Create item frames
        # for name, num, logo_file, _ in self.methods:
        #     frame = QFrame()
        #     frame.setFixedHeight(70)
        #     frame.setStyleSheet(self._frame_style(name == self.selected_method))
        #     fl = QHBoxLayout(frame)
        #     fl.setContentsMargins(12, 0, 12, 0)

        #     icon = QLabel()
        #     icon.setPixmap(
        #         QPixmap(os.path.join(base_dir, "..", "resources", "icons", "card.png"))
        #     )
        #     icon.setStyleSheet("border: none;")
        #     fl.addWidget(icon)

        #     txt = QVBoxLayout()
        #     lbl_name = QLabel(name)
        #     lbl_name.setFont(QFont(SETTINGS["font_family"], 12, QFont.Weight.Bold))
        #     lbl_name.setStyleSheet(
        #         f"""
        #             color: {SETTINGS['colors']['neutral']['Neutral 100']};
        #             border: none;
        #         """
        #     )
        #     lbl_num = QLabel(num)
        #     lbl_num.setFont(QFont(SETTINGS["font_family"], 10, QFont.Weight.Normal))
        #     lbl_num.setStyleSheet(
        #         f"""
        #             color: {SETTINGS['colors']['neutral']['Neutral 60']};
        #             border: none;
        #         """
        #     )
        #     txt.addWidget(lbl_name)
        #     txt.addWidget(lbl_num)
        #     fl.addLayout(txt)
        #     fl.addStretch()

        #     logo_lbl = QLabel()
        #     logo_lbl.setPixmap(
        #         QPixmap(
        #             os.path.join(base_dir, "..", "resources", "icons", logo_file)
        #         ).scaled(
        #             32,
        #             32,
        #             Qt.AspectRatioMode.KeepAspectRatio,
        #             Qt.TransformationMode.SmoothTransformation,
        #         )
        #     )
        #     logo_lbl.setStyleSheet("border: none;")
        #     fl.addWidget(logo_lbl)

        #     # Capture frame and name in callback
        #     frame.mousePressEvent = lambda event, n=name: self._on_method_click(n)

        #     self.method_frames[name] = frame
        #     cont_l.addWidget(frame)

        self._methods_container = cont_l

        # initial populate
        self._populate_methods()

        scroll.setWidget(cont)
        methods_layout.addWidget(scroll)
        main.addLayout(methods_layout)

        # ─── Add New Card Button ───────────────────────────────────────────────
        add_btn = QPushButton("Add New Card")
        add_btn.setFixedHeight(50)
        add_btn.setFont(QFont(SETTINGS["font_family"], 14, QFont.Weight.Bold))
        add_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #FE8C00;
                color: white;
                border-radius: 25px;
            }
            QPushButton:pressed {
                background-color: #e07f00;
            }
        """
        )
        add_btn.clicked.connect(lambda: self.addNewCard.emit())
        main.addWidget(add_btn)

    def _frame_style(self, selected: bool) -> str:
        border_color = (
            SETTINGS["colors"]["primary"]["hover"]
            if selected
            else SETTINGS["colors"]["neutral"]["Neutral 30"]
        )
        return (
            f"QFrame {{"
            f"color: {SETTINGS['colors']['neutral']['Neutral 100']};"
            f"border: 2px solid {border_color};"
            f"border-radius: 12px;"
            f"}}"
        )

    def _on_method_click(self, name: str):
        # Update selection
        if name == self.selected_method:
            return
        self.selected_method = name
        # Update frame styles
        for method_name, frame in self.method_frames.items():
            frame.setStyleSheet(self._frame_style(method_name == name))
        # Emit signal
        self.methodSelected.emit(name)

    def add_payment_method(self, pm: PaymentMethod):
        """
        Insert the new PaymentMethod into our on-screen list.
        """
        # Append to internal list
        self.methods.append(
            (
                pm.holder,  # display label
                pm.masked_number(),  # masked number
                self._detect_logo(pm),  # pick correct logo file
                False,  # not selected by default
            )
        )
        # Rebuild the scroll area
        self._populate_methods()

    def _detect_logo(self, pm: PaymentMethod) -> str:
        """Quick hack: choose logo based on first digit."""
        first = pm.number[0]
        if first == "4":
            return "visa.png"
        if first == "5":
            return "mastercard.png"
        # fallback
        return "card.png"

    def _populate_methods(self):
        """
        Clear out the current list and rebuild it from self.methods.
        """
        # remove old widgets
        for i in reversed(range(self._methods_container.count())):
            w = self._methods_container.itemAt(i).widget()
            if w:
                w.setParent(None)

        # re‐add from self.methods (name, num, logo, selected)
        for name, num, logo_file, selected in self.methods:
            frame = self._create_method_frame(name, num, logo_file, selected)
            self._methods_container.addWidget(frame)

    def _create_method_frame(self, name, num, logo_file, selected):
        """
        Your existing loop body refactored into a reusable factory.
        Returns the QFrame for one payment method.
        """
        base_dir = os.path.dirname(os.path.abspath(__file__))
        frame = QFrame()
        frame.setFixedHeight(70)
        frame.setStyleSheet(self._frame_style(name == self.selected_method))
        fl = QHBoxLayout(frame)
        fl.setContentsMargins(12, 0, 12, 0)

        icon = QLabel()
        icon.setPixmap(
            QPixmap(os.path.join(base_dir, "..", "resources", "icons", "card.png"))
        )
        icon.setStyleSheet("border: none;")
        fl.addWidget(icon)

        txt = QVBoxLayout()
        lbl_name = QLabel(name)
        lbl_name.setFont(QFont(SETTINGS["font_family"], 12, QFont.Weight.Bold))
        lbl_name.setStyleSheet(
            f"""
                color: {SETTINGS['colors']['neutral']['Neutral 100']};
                border: none;
            """
        )
        lbl_num = QLabel(num)
        lbl_num.setFont(QFont(SETTINGS["font_family"], 10, QFont.Weight.Normal))
        lbl_num.setStyleSheet(
            f"""
                color: {SETTINGS['colors']['neutral']['Neutral 60']};
                border: none;
            """
        )
        txt.addWidget(lbl_name)
        txt.addWidget(lbl_num)
        fl.addLayout(txt)
        fl.addStretch()

        logo_lbl = QLabel()
        logo_lbl.setPixmap(
            QPixmap(
                os.path.join(base_dir, "..", "resources", "icons", logo_file)
            ).scaled(
                32,
                32,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        )
        logo_lbl.setStyleSheet("border: none;")
        fl.addWidget(logo_lbl)

        # Capture frame and name in callback
        frame.mousePressEvent = lambda event, n=name: self._on_method_click(n)
        return frame
