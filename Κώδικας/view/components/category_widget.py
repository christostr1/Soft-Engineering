# view/components/category_widget.py


import os
from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QToolButton, QScrollArea, QFrame
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import Qt, QSize


class CategoryWidget(QWidget):
    """
    A horizontal scroll area displaying categories using CategoryCard.
    """
    def __init__(self, categories, parent=None):
        """
        :param categories: List of tuples (icon_path, label_text)
        """
        super().__init__(parent)
        self.categories = categories

        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)

        # === Title Row ===
        title_row = QHBoxLayout()
        title = QLabel("Find by Category")
        title.setFont(QFont("Inter", 14, QFont.Weight.Bold))
        title.setStyleSheet("color: #1e1e1e;")

        # You can keep "See All" as a plain text button (using QToolButton or QPushButton)
        see_all = QToolButton()
        see_all.setText("See All")
        see_all.setStyleSheet("color: #FE8C00; font-size: 13px; background: transparent; border: none;")
        title_row.addWidget(title)
        title_row.addStretch()
        title_row.addWidget(see_all)
        main_layout.addLayout(title_row)

        # === Scrollable Categories ===
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFixedHeight(80)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        scroll_container = QFrame()
        row_layout = QHBoxLayout(scroll_container)
        row_layout.setContentsMargins(0, 0, 0, 0)
        row_layout.setSpacing(12)



        for icon_path, label, active in self.categories:
            btn = QToolButton()
            # Make the icon appear above the text.
            btn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
            btn.setFixedSize(70, 70)
            btn.setCheckable(True)
            btn.setChecked(active)
            btn.setIcon(QIcon(icon_path))
            btn.setIconSize(QSize(32, 32))
            btn.setText(label)
            btn.setStyleSheet(f"""
                QToolButton {{
                    background-color: {"#FE8C00" if active else "#FFFFFF"};
                    color: {"#FFFFFF" if active else "#1E1E1E"};
                    border: 1px solid #EEE;
                    border-radius: 16px;
                    font-size: 13px;
                }}
            """)
            row_layout.addWidget(btn)

        scroll_area.setWidget(scroll_container)
        main_layout.addWidget(scroll_area)

        self.setLayout(main_layout)

