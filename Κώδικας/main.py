import sys
import logging
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PyQt6.QtGui import QFont
from colorama import Fore, Style, init

# Import configuration settings.
from config.settings import SETTINGS

# Import screens.
from view.home_screen import HomeScreen
from view.search_screen import SearchScreen
from view.cart_screen import CartScreen
from view.messages_screen import MessagesScreen
from view.profile_screen import ProfileScreen
from view.product_details_screen import ProductDetailsScreen
from view.login_screen import LoginScreen
from view.register_screen import RegisterScreen
from view.edit_profile_screen import EditProfileScreen
from view.payment_methods_screen import PaymentMethodsScreen
from view.add_card_dialog import AddCardDialog
from view.recommendation_screen import RecommendationScreen

# Import navigation controller.
from controller.navigation_controller import NavigationController

# Import custom widgets.
from model.payment_method import PaymentMethod

from controller.navigation_controller import NavigationController
from model.errors import MissingNameError
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QMessageBox

# ----------------------------------------------------------------
# Setup Logging with Colorama
# ----------------------------------------------------------------
init(autoreset=True)


class ColoredFormatter(logging.Formatter):
    """
    Custom logging formatter that adds colors based on log levels.
    """

    LEVEL_COLORS = {
        logging.DEBUG: Fore.GREEN,
        logging.INFO: Fore.WHITE,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.RED,
    }

    def format(self, record):
        color = self.LEVEL_COLORS.get(record.levelno, Fore.WHITE)
        record.levelname = f"{color}{record.levelname}{Style.RESET_ALL}"
        return super().format(record)


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
log_format = "%(asctime)s - %(levelname)s - %(message)s"
console_handler.setFormatter(ColoredFormatter(log_format))
logger.addHandler(console_handler)

logging.debug(
    "Custom colored logging is set up with configuration settings integrated."
)

# ----------------------------------------------------------------
# MainWindow Definition
# ----------------------------------------------------------------


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initialize_window()
        self.create_screens()
        self.setup_navigation_controller()
        self.connect_signals()
        self.delivery_persons: list[DeliveryPerson] = []

    def initialize_window(self):
        """Set window title, size, and stylesheet."""
        self.setWindowTitle("SmartBite")
        self.setMinimumSize(400, 800)  # Using minimum size; adjust as needed.
        neutral_surface = SETTINGS["colors"]["neutral"]["Neutral 20"]
        self.setStyleSheet(f"background-color: {neutral_surface};")
        logging.debug(
            "Main window initialized with title 'SmartBite' and size 400x800."
        )
        logging.debug(
            f"Main window stylesheet set with background color: {neutral_surface}"
        )

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

    def create_screens(self):
        """Instantiate all application screens."""
        self.login_screen = LoginScreen()
        self.home_screen = HomeScreen()
        self.search_screen = SearchScreen()
        self.cart_screen = CartScreen()
        self.messages_screen = MessagesScreen()
        self.profile_screen = ProfileScreen()
        self.register_screen = RegisterScreen()
        self.edit_profile_screen = EditProfileScreen()
        self.payment_methonds_screen = PaymentMethodsScreen()
        self.add_card_dialog = AddCardDialog()
        self.recommendation_screen = RecommendationScreen()
        self.nav_controller = NavigationController(self.stacked_widget)

    def setup_navigation_controller(self):
        """Create and register tab screens with the NavigationController."""
        self.nav_controller = NavigationController(self.stacked_widget)
        # Register persistent tab screens.
        self.nav_controller.register_screen("home", self.home_screen)
        self.nav_controller.register_screen("search", self.search_screen)
        self.nav_controller.register_screen("cart", self.cart_screen)
        self.nav_controller.register_screen("messages", self.messages_screen)
        self.nav_controller.register_screen("profile", self.profile_screen)
        self.nav_controller.register_screen("login", self.login_screen)
        self.nav_controller.register_screen("register", self.register_screen)
        self.nav_controller.register_screen("edit_profile", self.edit_profile_screen)
        self.nav_controller.register_screen(
            "payment_methonds", self.payment_methonds_screen
        )
        self.nav_controller.register_screen("add_card_dialog", self.add_card_dialog)
        self.nav_controller.register_screen(
            "recommendations", self.recommendation_screen
        )

        # Start by displaying the Home screen.
        self.stacked_widget.setCurrentWidget(self.recommendation_screen)

    def connect_signals(self):
        """Connect signals between screens and the navigation controller."""
        # Connect bottom nav signals from each tab screen to the navigation controller.
        self.home_screen.bottom_nav.tab_clicked.connect(
            self.nav_controller.on_tab_clicked
        )
        self.cart_screen.bottom_nav.tab_clicked.connect(
            self.nav_controller.on_tab_clicked
        )
        self.messages_screen.bottom_nav.tab_clicked.connect(
            self.nav_controller.on_tab_clicked
        )
        self.profile_screen.bottom_nav.tab_clicked.connect(
            self.nav_controller.on_tab_clicked
        )

        # Connect product click signal from HomeScreen's product grid to show product details.
        self.home_screen.product_grid.productClicked.connect(self.show_product_details)
        self.home_screen.top_bar.searchClicked.connect(
            lambda: self.nav_controller.on_tab_clicked("search")
        )

        # Connect back button signals for dynamic screens.
        self.profile_screen.backClicked.connect(self.nav_controller.on_back_clicked)
        self.cart_screen.backClicked.connect(self.nav_controller.on_back_clicked)
        self.messages_screen.backClicked.connect(self.nav_controller.on_back_clicked)
        self.search_screen.back.connect(self.nav_controller.on_back_clicked)
        self.edit_profile_screen.back.connect(self.nav_controller.on_back_clicked)
        self.payment_methonds_screen.back.connect(self.nav_controller.on_back_clicked)
        # Connect LoginScreen navigation signals.
        self.login_screen.loginSuccessful.connect(
            lambda: self.nav_controller.on_tab_clicked("home")
        )
        self.login_screen.goToRegister.connect(
            lambda: self.nav_controller.on_tab_clicked("register")
        )
        # Connect RegisterScreen navigation signals.
        self.register_screen.goToLogin.connect(
            lambda: self.nav_controller.on_tab_clicked("login")
        )
        # Connect ProfileScreen sign out signal.
        self.profile_screen.signOutClicked.connect(
            lambda: self.nav_controller.on_tab_clicked("login")
        )

        self.payment_methonds_screen.addNewCard.connect(self.open_add_card_dialog)
        self.add_card_dialog.saved.connect(self.handle_new_card)

        # from Home: when app starts, go to recommendations
        self.home_screen.top_bar.searchClicked.connect(
            lambda: self.nav_controller.on_tab_clicked("recommendations")
        )
        # back from recommendations
        self.recommendation_screen.back.connect(self.nav_controller.on_back_clicked)

    def open_add_card_dialog(self):
        """Show the AddCardDialog as a modal dialog."""
        # You can recreate it each time, or reuse self.add_card_dialog
        dlg = AddCardDialog(self)
        dlg.saved.connect(self.handle_new_card)  # so you can react when Save is clicked
        dlg.exec()  # blocks until dialog closes

    def handle_new_card(self, data: dict):
        """
        data == {
           'holder': str,
           'number': str,
           'expiry': str,
           'cvv'   : str,
        }
        """
        # 1) instantiate & validate
        pm = PaymentMethod(
            holder=data["holder"],
            number=data["number"],
            expiry=data["expiry"],
            cvv=data["cvv"],
        )
        try:
            pm.validate()
        except Exception as e:
            # you might show a QMessageBox here
            logging.error(f"Failed to add card: {e}")
            return

        # 2) add to PaymentMethodsScreen
        self.payment_methonds_screen.add_payment_method(pm)

    def show_product_details(self, product_data: dict):
        """
        Slot to handle a product click.
        Creates a ProductDetailsScreen, connects its back signal,
        and adds it as a dynamic screen.
        """
        product_details_screen = ProductDetailsScreen(product_data)
        product_details_screen.backClicked.connect(self.nav_controller.on_back_clicked)
        self.nav_controller.add_screen("details", product_details_screen)
        logging.debug("Product details screen displayed.")




# ----------------------------------------------------------------
# Application Entry Point
# ----------------------------------------------------------------


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    logging.debug("Application started; MainWindow is now visible.")
    sys.exit(app.exec())
