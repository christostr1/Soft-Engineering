# view/components/base_screen.py
from PyQt6.QtWidgets import QWidget


class BaseScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Place common functionality or styling for all screens here.
