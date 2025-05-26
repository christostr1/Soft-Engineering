import os
import logging

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QHBoxLayout, QFrame, QToolButton, QSizePolicy
)
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from PyQt6.QtGui import QFont, QIcon
from config.settings import SETTINGS

class LoginScreen(QWidget):
    # Custom signals for navigation.
    loginSuccessful = pyqtSignal()
    goToRegister = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        logging.debug("Initializing LoginScreen.")
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(8)

        # Title
        title_label = QLabel("Login to your account.")
        title_label.setFont(QFont(SETTINGS["font_family"], 20, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #1E1E1E;")
        main_layout.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignLeft)

        # Subtitle
        subtitle_label = QLabel("Please sign in to your account")
        subtitle_label.setFont(QFont(SETTINGS["font_family"], 12))
        subtitle_label.setStyleSheet("color: #9A9A9A;")
        main_layout.addWidget(subtitle_label, alignment=Qt.AlignmentFlag.AlignLeft)

        # Email Field
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter Email")
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

        # Password Field with Toggle
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

        # Forgot Password Link
        forgot_password_btn = QPushButton("Forgot password?")
        forgot_password_btn.setStyleSheet("""
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
        forgot_password_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        main_layout.addWidget(forgot_password_btn, alignment=Qt.AlignmentFlag.AlignRight)

        # Sign In Button
        sign_in_btn = QPushButton("Sign In")
        sign_in_btn.setFont(QFont(SETTINGS["font_family"], 14, QFont.Weight.Bold))
        sign_in_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #FE8C00;
                color: white;
                border-radius: 20px;
                padding: 12px;
            }}
            QPushButton:hover {{
                background-color: {SETTINGS['colors'].get('primary', {}).get('hover', '#FF9E22')};
            }}
        """)
        sign_in_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        # Connect sign in button click to our slot that will emit the navigation signal.
        sign_in_btn.clicked.connect(self.on_sign_in)
        main_layout.addWidget(sign_in_btn)

        # "Or sign in with" Section
        or_label = QLabel("Or sign in with")
        or_label.setFont(QFont(SETTINGS["font_family"], 12))
        or_label.setStyleSheet("color: #9A9A9A;")
        or_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(or_label)

        # Social Buttons
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

        # Register Section ("Don't have an account? Register")
        register_container = QFrame()
        register_layout = QHBoxLayout(register_container)
        register_layout.setContentsMargins(0, 0, 0, 0)
        register_layout.setSpacing(4)
        register_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_no_account = QLabel("Don't have an account?")
        lbl_no_account.setFont(QFont(SETTINGS["font_family"], 12))
        lbl_no_account.setStyleSheet("color: #9A9A9A;")
        btn_register = QPushButton("Register")
        btn_register.setStyleSheet("""
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
        btn_register.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_register.clicked.connect(self.on_register)
        register_layout.addWidget(lbl_no_account)
        register_layout.addWidget(btn_register)
        main_layout.addWidget(register_container)

        logging.debug("LoginScreen UI setup completed.")

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

    def on_sign_in(self):
        """
        Slot executed when the Sign In button is pressed.
        Emits a signal to navigate to the Home screen.
        """
        logging.debug("Sign In button pressed. Emitting loginSuccessful signal.")
        # Here you could add authentication logic before emitting the signal.
        self.loginSuccessful.emit()

    def on_register(self):
        """
        Slot executed when the Register button is pressed.
        Emits a signal to navigate to the Register screen.
        """
        logging.debug("Register button pressed. Emitting goToRegister signal.")
        self.goToRegister.emit()
