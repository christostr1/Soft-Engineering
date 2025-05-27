import os
from typing import List
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QFrame,
    QMessageBox,
    QToolButton,
)
from PyQt6.QtGui import QFont, QIcon, QPixmap
from PyQt6.QtCore import Qt, QSize, pyqtSignal

from model.preferences import Preferences
from model.filters import Filters
from model.recommendation_algorithm import RecommendationAlgorithm
from model.menu_item import MenuItem
from view.components.product_card import ProductCard
from config.settings import SETTINGS


class RecommendationScreen(QWidget):
    back = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.algorithm = RecommendationAlgorithm()
        self.setup_ui()

    def setup_ui(self):
        main = QVBoxLayout(self)
        main.setContentsMargins(16, 16, 16, 16)
        main.setSpacing(12)

        # ── Header ───────────────────────────────────────
        header = QHBoxLayout()
        btn_back = QToolButton()
        btn_back.setIcon(QIcon("resources/icons/Back2.png"))
        btn_back.setIconSize(QSize(40, 40))
        btn_back.setStyleSheet("border: none;")
        btn_back.clicked.connect(lambda: self.back.emit())
        title_label = QLabel("Προτιμήσεις & Προτάσεις")
        title_label.setFont(QFont(SETTINGS["font_family"], 14, QFont.Weight.Bold))
        title_label.setStyleSheet(
            f"color: {SETTINGS['colors']['neutral']['Neutral 100']};"
        )
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.addWidget(btn_back)
        header.addStretch()
        header.addWidget(title_label)
        header.addStretch()
        header.addSpacing(36)
        main.addLayout(header)

        # ── Preferences Form ────────────────────────────
        form = QVBoxLayout()
        # Cuisine
        self.cuisine_cb = QComboBox()
        self.cuisine_cb.addItems(
            ["Μεσογειακή", "Ιταλική", "Ασιατική", "Γρήγορο φαγητό"]
        )
        self.cuisine_cb.setStyleSheet(
            f"color: {SETTINGS['colors']['neutral']['Neutral 100']};"
        )
        form.addWidget(self.labeled("Είδος Κουζίνας", self.cuisine_cb))
        # Meal Type
        self.meal_cb = QComboBox()
        self.meal_cb.addItems(["Μεσημεριανό", "Βραδινό", "Σνακ", "Πρωινό"])
        self.meal_cb.setStyleSheet(
            f"color: {SETTINGS['colors']['neutral']['Neutral 100']};"
        )

        form.addWidget(self.labeled("Τύπος Γεύματος", self.meal_cb))
        # Filters: price, distance, time
        self.price_le = QLineEdit()
        self.price_le.setPlaceholderText("π.χ. 10.0")
        self.price_le.setFixedHeight(32)
        self.price_le.setStyleSheet(
            f"color: {SETTINGS['colors']['neutral']['Neutral 100']};"
        )
        form.addWidget(self.labeled("Max Τιμή (€)", self.price_le))
        self.dist_le = QLineEdit()
        self.dist_le.setPlaceholderText("π.χ. 2.5")
        self.dist_le.setFixedHeight(32)
        self.dist_le.setStyleSheet(
            f"color: {SETTINGS['colors']['neutral']['Neutral 100']};"
        )
        form.addWidget(self.labeled("Max Απόσταση (km)", self.dist_le))
        self.time_le = QLineEdit()
        self.time_le.setPlaceholderText("π.χ. 30")
        self.time_le.setFixedHeight(32)
        self.time_le.setStyleSheet(
            f"color: {SETTINGS['colors']['neutral']['Neutral 100']};"
        )
        form.addWidget(self.labeled("Max Χρόνος (λεπτά)", self.time_le))

        # Confirm button
        btn_layout = QHBoxLayout()
        confirm = QPushButton("Επιβεβαίωση")
        confirm.setFixedHeight(40)
        confirm.setStyleSheet(
            f"""
            background-color: {SETTINGS['colors']['primary']['hover']};
            color: {SETTINGS['colors']['neutral']['Neutral 100']}; 
            border-radius: 8px;
        """
        )
        confirm.clicked.connect(self.on_confirm)
        btn_layout.addStretch()
        btn_layout.addWidget(confirm)
        btn_layout.addStretch()

        form.addLayout(btn_layout)
        main.addLayout(form)

        # ── Recommendations Area ────────────────────────
        self.rec_area = QScrollArea()
        self.rec_area.setWidgetResizable(True)
        self.rec_container = QWidget()
        self.rec_layout = QVBoxLayout(self.rec_container)
        self.rec_layout.setSpacing(10)
        self.rec_area.setWidget(self.rec_container)
        main.addWidget(self.rec_area, stretch=1)

    def labeled(self, label_txt, widget):
        fr = QFrame()
        lay = QVBoxLayout(fr)
        lbl = QLabel(label_txt)
        lbl.setFont(QFont(SETTINGS["font_family"], 12))
        lbl.setStyleSheet(f"color: {SETTINGS['colors']['neutral']['Neutral 100']};")
        lay.addWidget(lbl)
        lay.addWidget(widget)
        return fr

    def on_confirm(self):
        # gather inputs
        try:
            prefs = Preferences(
                cuisine=self.cuisine_cb.currentText(),
                meal_type=self.meal_cb.currentText(),
            )
            fltrs = Filters(
                max_price=float(self.price_le.text()),
                max_distance=float(self.dist_le.text()),
                max_time=int(self.time_le.text()),
            )
        except ValueError:
            QMessageBox.warning(
                self,
                "Σφάλμα Εισόδου",
                "Παρακαλώ εισάγετε αριθμούς για τιμή/απόσταση/χρόνο.",
            )
            return

        # run algorithm
        try:
            self.algorithm.analyzeBehavior(None)  # user not modeled here
            recs = self.algorithm.getRecommendations(None, prefs, fltrs)
        except Exception:
            QMessageBox.critical(
                self, "Σφάλμα", "Πρόβλημα με τον αλγόριθμο. Δοκιμάστε ξανά."
            )
            return

        # display
        # clear old
        for i in reversed(range(self.rec_layout.count())):
            w = self.rec_layout.itemAt(i).widget()
            if w:
                w.setParent(None)

        # add cards
        for item in recs:
            # create a minimal card: name + price
            card = ProductCard(
                image=os.path.join("resources", "images", item.image),
                title=item.name,
                rating="",
                distance="",
                price=f"€{item.price:.2f}",
            )
            self.rec_layout.addWidget(card)
