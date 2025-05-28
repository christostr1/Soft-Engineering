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
    QFileDialog,
)
from PyQt6.QtGui import QPixmap, QFont, QIcon
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from config.settings import SETTINGS


class EditProfileScreen(QWidget):
    back = pyqtSignal()
    saveClicked = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.profile_pic_path = None
        self.setup_ui()

    def setup_ui(self):
        # self.setStyleSheet("background-color: white;")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Header
        header = QHBoxLayout()
        # Back Button.
        back_btn = QPushButton()
        back_btn.setIcon(QIcon("resources/icons/Back2.png"))
        back_btn.setIconSize(QSize(40, 40))
        back_btn.setStyleSheet("border: none;")
        back_btn.clicked.connect(lambda: self.back.emit())

        title_label = QLabel("Personal Date")
        title_label.setFont(QFont(SETTINGS["font_family"], 16, QFont.Weight.Bold))
        title_label.setStyleSheet(
            f"color: {SETTINGS['colors']['neutral']['Neutral 100']};"
        )
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        header.addWidget(back_btn)
        header.addStretch()
        header.addWidget(title_label)
        header.addStretch()
        header.addSpacing(36)
        main_layout.addLayout(header)

        main_layout.addSpacing(10)

        # Profile Image
        img_container = QFrame()
        img_layout = QVBoxLayout(img_container)
        img_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.img_label = QLabel()
        default_img_path = os.path.join(
            "resources", "images", "profile_avatar.png"
        )  # Replace with your default image path
        self.set_profile_image(default_img_path)
        img_layout.addWidget(self.img_label)

        main_layout.addWidget(img_container, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addSpacing(10)

        # Scrollable form area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        form_widget = QWidget()
        form_layout = QVBoxLayout(form_widget)
        form_layout.setSpacing(15)

        # Form Fields
        self.fullname_input = self.create_input("Full Name", "")
        self.birthdate_input = self.create_input("Date of birth", "")
        self.gender_input = self.create_dropdown("Gender", ["Male", "Female", "Other"])
        self.phone_input = self.create_input("Phone", "")
        self.email_input = self.create_input("Email", "")

        form_layout.addWidget(self.fullname_input)
        form_layout.addWidget(self.birthdate_input)
        form_layout.addWidget(self.gender_input)
        form_layout.addWidget(self.phone_input)
        form_layout.addWidget(self.email_input)

        form_layout.addStretch()
        scroll.setWidget(form_widget)
        main_layout.addWidget(scroll)

        # Save Button
        save_btn = QPushButton("Save")
        save_btn.setFixedHeight(50)
        save_btn.setFont(QFont("Inter", 14, QFont.Weight.Bold))
        save_btn.setStyleSheet(
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
        save_btn.clicked.connect(self.on_save_clicked)

        main_layout.addWidget(save_btn)

    def create_input(self, label_text, default_value):
        frame = QFrame()
        layout = QVBoxLayout(frame)
        layout.setSpacing(5)

        label = QLabel(label_text)
        label.setFont(QFont(SETTINGS["font_family"], 13))
        label.setStyleSheet("color: #000;")
        input_field = QLineEdit()
        input_field.setText(default_value)
        input_field.setFixedHeight(45)
        input_field.setStyleSheet(
            """
                color: #000;
                border: 1px solid #CCC;
                border-radius: 10px;
                padding-left: 10px;
                font-size: 14px;
            """
        )

        layout.addWidget(label)
        layout.addWidget(input_field)
        return frame

    def create_dropdown(self, label_text, options):
        frame = QFrame()
        layout = QVBoxLayout(frame)
        layout.setSpacing(5)

        label = QLabel(label_text)
        label.setFont(QFont(SETTINGS["font_family"], 13))
        label.setStyleSheet("color: #000;")
        dropdown = QComboBox()
        dropdown.addItems(options)
        dropdown.setFixedHeight(45)
        dropdown.setStyleSheet(
            """
                QComboBox {
                    /* the line-edit / current-selection styling */
                    color: #000;
                    border: 1px solid #CCC;
                    border-radius: 10px;
                    padding-left: 10px;
                    font-size: 14px;
                }
                /* this styles the drop-down list */
                QComboBox QAbstractItemView {
                    color: #000;                /* text color of items */
                    background-color: #FFFFFF;     /* background of the list */
                    selection-background-color: #FE8C00;
                    selection-color: #FFFFFF;
                }
            """
        )

        layout.addWidget(label)
        layout.addWidget(dropdown)
        return frame

    def set_profile_image(self, img_path):
        pixmap = QPixmap(img_path).scaled(
            120,
            120,
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation,
        )
        self.img_label.setPixmap(pixmap)
        self.img_label.setFixedSize(120, 120)
        self.img_label.setStyleSheet("border-radius: 60px;")
        self.profile_pic_path = img_path

    def change_profile_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Profile Picture", "", "Images (*.png *.jpg *.jpeg)"
        )
        if file_path:
            self.set_profile_image(file_path)

    def on_save_clicked(self):
        profile_data = {
            "fullname": self.fullname_input.findChild(QLineEdit).text(),
            "birthdate": self.birthdate_input.findChild(QLineEdit).text(),
            "gender": self.gender_input.findChild(QComboBox).currentText(),
            "phone": self.phone_input.findChild(QLineEdit).text(),
            "email": self.email_input.findChild(QLineEdit).text(),
            "profile_picture": self.profile_pic_path,
        }
        self.saveClicked.emit(profile_data)
