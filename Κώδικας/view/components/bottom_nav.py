# view/components/bottom_nav.py

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QToolButton
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize, pyqtSignal, Qt
from config.settings import SETTINGS

class BottomNav(QWidget):
    """
    Bottom navigation bar with tabs for navigation.
    Emitting signals so that MainWindow (or controllers) can handle the screen changes.
    """

    # Signal with the name of the tab the user clicked
    tab_clicked = pyqtSignal(str)

    def __init__(self, current_tab: str = "home", parent=None):
        super().__init__(parent)
        # Ensure that the background is styled using the widget's style sheet.
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.current_tab = current_tab
        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Home button
        self.home_button = QToolButton()
        self.home_button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.home_button.setFixedSize(70, 70)
        self.home_button.setText("Home")
        self.home_button.setIcon(QIcon("resources/icons/home.png"))
        self.home_button.setIconSize(QSize(32, 32))
        self.home_button.setObjectName("home")
        self.home_button.clicked.connect(self.handle_tab_clicked)
        layout.addWidget(self.home_button)

        # Cart button
        self.search_button = QToolButton()
        self.search_button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.search_button.setFixedSize(70, 70)
        self.search_button.setText("Cart")
        self.search_button.setIcon(QIcon("resources/icons/bag.png"))
        self.search_button.setIconSize(QSize(32, 32))
        self.search_button.setObjectName("cart")
        self.search_button.clicked.connect(self.handle_tab_clicked)
        layout.addWidget(self.search_button)

        # Messages button
        self.favorites_button = QToolButton()
        self.favorites_button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.favorites_button.setFixedSize(70, 70)
        self.favorites_button.setText("Messages")
        self.favorites_button.setIcon(QIcon("resources/icons/chat.png"))
        self.favorites_button.setIconSize(QSize(32, 32))
        self.favorites_button.setObjectName("messages")
        self.favorites_button.clicked.connect(self.handle_tab_clicked)
        layout.addWidget(self.favorites_button)

        # Profile button
        self.profile_button = QToolButton()
        self.profile_button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.profile_button.setFixedSize(70, 70)
        self.profile_button.setText("Profile")
        self.profile_button.setIcon(QIcon("resources/icons/profile.png"))
        self.profile_button.setIconSize(QSize(32, 32))
        self.profile_button.setObjectName("profile")
        self.profile_button.clicked.connect(self.handle_tab_clicked)
        layout.addWidget(self.profile_button)

        self.setLayout(layout)
        self.update_selected_tab()

    def handle_tab_clicked(self):
        clicked_button = self.sender()
        if clicked_button:
            self.current_tab = clicked_button.objectName()
            self.tab_clicked.emit(self.current_tab)
            self.update_selected_tab()

    def update_selected_tab(self):
        # Use the "hover" color from your settings to indicate selection.
        highlight_color = SETTINGS["colors"]["primary"]["hover"]
        default_color = "transparent"
        for button in (self.home_button, self.search_button, self.favorites_button, self.profile_button):
            if button.objectName() == self.current_tab:
                button.setStyleSheet(f"background-color: {highlight_color};")
            else:
                button.setStyleSheet(f"background-color: {default_color};")
