# view/register_screen.py

import logging
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QHBoxLayout, QFrame, QToolButton, QSizePolicy, QCheckBox
)
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from PyQt6.QtGui import QFont, QIcon

from config.settings import SETTINGS

class RegisterScreen(QWidget):
    """
    A Register screen replicating your design with:
      - Title and subtitle
      - Email, User Name, Password fields (password toggle)
      - A checkbox for Terms of Service and Privacy
      - 'Register' button
      - 'Or sign in with' icons
      - 'Don't have an account? Sign In'
    """

    # Signals to navigate and process registration events
    registerSubmitted = pyqtSignal()
    goToLogin = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        logging.debug("Initializing RegisterScreen.")
        self.setup_ui()

    def setup_ui(self):
        """
        Builds the entire UI for the register screen.
        """
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(8)

        # 1. Title
        title_label = QLabel("Create your new account")
        title_label.setFont(QFont(SETTINGS["font_family"], 20, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #1E1E1E;")
        main_layout.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignLeft)

        # 2. Subtitle
        subtitle_label = QLabel("Create an account to start looking for the food you like")
        subtitle_label.setFont(QFont(SETTINGS["font_family"], 12))
        subtitle_label.setStyleSheet("color: #9A9A9A;")
        main_layout.addWidget(subtitle_label, alignment=Qt.AlignmentFlag.AlignLeft)

        # 3. Email Address
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("ZedZilean@gmail.com")
        self.email_input.setFont(QFont(SETTINGS["font_family"], 12))
        self.email_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                padding: 12px;
                color: #1E1E1E;
            }
        """)
        main_layout.addWidget(self.email_input)

        # 4. User Name
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("User Name")
        self.username_input.setFont(QFont(SETTINGS["font_family"], 12))
        self.username_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                padding: 12px;
                color: #1E1E1E;
            }
        """)
        main_layout.addWidget(self.username_input)

        # 5. Password with toggle
        password_container = QFrame()
        pass_layout = QHBoxLayout(password_container)
        pass_layout.setContentsMargins(0, 0, 0, 0)
        pass_layout.setSpacing(0)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setFont(QFont(SETTINGS["font_family"], 12))
        self.password_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                padding: 12px;
                color: #1E1E1E;
            }
        """)
        pass_layout.addWidget(self.password_input, stretch=1)

        self.toggle_password_btn = QToolButton()
        self.toggle_password_btn.setIcon(QIcon("resources/icons/eye_off.png"))
        self.toggle_password_btn.setIconSize(QSize(24, 24))
        self.toggle_password_btn.setStyleSheet("border: none; background: transparent;")
        self.toggle_password_btn.clicked.connect(self.toggle_password_visibility)
        pass_layout.addWidget(self.toggle_password_btn)

        main_layout.addWidget(password_container)

        # 6. Terms of Service and Privacy Policy
        tos_layout = QHBoxLayout()
        tos_layout.setContentsMargins(0, 0, 0, 0)
        tos_layout.setSpacing(8)

        self.tos_checkbox = QCheckBox()
        self.tos_checkbox.setText("I Agree with")
        self.tos_checkbox.setFont(QFont(SETTINGS["font_family"], 12))
        self.tos_checkbox.setStyleSheet("color: #1E1E1E;")

        tos_layout.addWidget(self.tos_checkbox)

        tos_label = QLabel("Terms of Service and Privacy Policy")
        tos_label.setFont(QFont(SETTINGS["font_family"], 12))
        tos_label.setStyleSheet("""
            color: #FE8C00; 
        """)
        # Could connect a link if you want clickable TOS, e.g. tos_label.linkActivated.connect(...)
        tos_layout.addWidget(tos_label, alignment=Qt.AlignmentFlag.AlignLeft)

        main_layout.addLayout(tos_layout)

        # 7. Register Button
        register_btn = QPushButton("Register")
        register_btn.setFont(QFont(SETTINGS["font_family"], 14, QFont.Weight.Bold))
        register_btn.setStyleSheet("""
            QPushButton {
                background-color: #FE8C00;
                color: white;
                border-radius: 20px;
                padding: 12px;
            }
            QPushButton:hover {
                background-color: #FF9E22;
            }
        """)
        register_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        register_btn.clicked.connect(self.on_register_clicked)
        main_layout.addWidget(register_btn)

        # 8. Or sign in with
        or_label = QLabel("Or sign in with")
        or_label.setFont(QFont(SETTINGS["font_family"], 12))
        or_label.setStyleSheet("color: #9A9A9A;")
        or_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(or_label)

        # Social buttons row
        social_container = QFrame()
        social_layout = QHBoxLayout(social_container)
        social_layout.setContentsMargins(0, 0, 0, 0)
        social_layout.setSpacing(16)
        social_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        google_btn = QToolButton()
        google_btn.setIcon(QIcon("resources/icons/google.png"))
        google_btn.setIconSize(QSize(28, 28))
        google_btn.setStyleSheet("border: none; background: transparent;")

        facebook_btn = QToolButton()
        facebook_btn.setIcon(QIcon("resources/icons/facebook.png"))
        facebook_btn.setIconSize(QSize(28, 28))
        facebook_btn.setStyleSheet("border: none; background: transparent;")

        apple_btn = QToolButton()
        apple_btn.setIcon(QIcon("resources/icons/apple.png"))
        apple_btn.setIconSize(QSize(28, 28))
        apple_btn.setStyleSheet("border: none; background: transparent;")

        social_layout.addWidget(google_btn)
        social_layout.addWidget(facebook_btn)
        social_layout.addWidget(apple_btn)
        main_layout.addWidget(social_container)

        # 9. Bottom: "Don't have an account? Sign In"
        sign_in_container = QFrame()
        sign_in_layout = QHBoxLayout(sign_in_container)
        sign_in_layout.setContentsMargins(0, 0, 0, 0)
        sign_in_layout.setSpacing(4)
        sign_in_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        lbl_has_account = QLabel("Don't have an account?")
        lbl_has_account.setFont(QFont(SETTINGS["font_family"], 12))
        lbl_has_account.setStyleSheet("color: #9A9A9A;")

        btn_sign_in = QPushButton("Sign In")
        btn_sign_in.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #FE8C00;
                border: none;
                font-size: 12px;
            }
            QPushButton:hover {
                text-decoration: underline;
            }
        """)
        btn_sign_in.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_sign_in.clicked.connect(self.on_sign_in_clicked)

        sign_in_layout.addWidget(lbl_has_account)
        sign_in_layout.addWidget(btn_sign_in)
        main_layout.addWidget(sign_in_container)

        logging.debug("RegisterScreen UI setup completed.")

    def toggle_password_visibility(self):
        """
        Toggles the echo mode of the password field and swaps the eye icon.
        """
        if self.password_input.echoMode() == QLineEdit.EchoMode.Password:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
            self.toggle_password_btn.setIcon(QIcon("resources/icons/eye_on.png"))
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.toggle_password_btn.setIcon(QIcon("resources/icons/eye_off.png"))

    def on_register_clicked(self):
        """
        Slot called when the 'Register' button is pressed.
        Emitted as 'registerSubmitted' signal for external navigation/logic.
        """
        logging.debug("Register button pressed. Emitting registerSubmitted signal.")
        # Optionally add validations, terms-of-service checks, etc.
        self.registerSubmitted.emit()

    def on_sign_in_clicked(self):
        """
        Slot called when 'Sign In' is pressed, for users who already have an account.
        """
        logging.debug("Sign In button in RegisterScreen pressed. Emitting goToLogin signal.")
        self.goToLogin.emit()
