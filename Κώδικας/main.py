# main.py
import sys
import logging
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QPushButton
from PyQt6.QtGui import QFont
from view.home_screen import HomeScreen
from view.search_screen import SearchScreen
from view.product_details_screen import ProductDetailsScreen
from view.cart import CartScreen
from view.messages_screen import MessagesScreen
from view.profile_screen import ProfileScreen

# Import configuration settings for fonts and colors
from config.settings import SETTINGS

# Import colorama for colored logging output
from colorama import Fore, Style, init

from controller.navigation_controller import NavigationController

# Initialize colorama with autoreset to ensure colors are reset after each log message
init(autoreset=True)


class ColoredFormatter(logging.Formatter):
    """
    Custom logging formatter to add colors based on the log level.
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


# Configure root logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Define log format
log_format = "%(asctime)s - %(levelname)s - %(message)s"
formatter = ColoredFormatter(log_format)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

logging.debug("Custom colored logging is set up with configuration settings integrated.")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Set the window title and initial size
        self.setWindowTitle("SmartBite")
        self.setMinimumSize(400, 800)
        logging.debug("Main window initialized with title 'SmartBite' and size 400x800.")

        # Set a sample stylesheet using the configured primary surface color
        # (Update with appropriate configuration as needed)
        neutral_surface = SETTINGS["colors"]["neutral"]["Neutral 20"]
        self.setStyleSheet(f"background-color: {neutral_surface};")
        logging.debug(f"Main window stylesheet set with background color: {neutral_surface}")

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Create screens (ensure they are implemented correctly).
        self.home_screen = HomeScreen()
        self.search_screen = SearchScreen()
        self.cart_screen = CartScreen()
        self.messages_screen = MessagesScreen()
        self.profile_screen = ProfileScreen()

        # Create and set up the navigation controller.
        self.nav_controller = NavigationController(self.stacked_widget)

        # Register tab screens.
        self.nav_controller.register_screen("home", self.home_screen)
        self.nav_controller.register_screen("cart", self.cart_screen)
        self.nav_controller.register_screen("messages", self.messages_screen)
        self.nav_controller.register_screen("profile", self.profile_screen)

        # Start by showing the home screen.
        self.stacked_widget.setCurrentWidget(self.profile_screen)

        # Connect product clicks from the home screen's product grid to show product details.
        self.home_screen.product_grid.productClicked.connect(self.show_product_details)
        self.messages_screen.bottom_nav.tab_clicked.connect(self.nav_controller.on_tab_clicked)
        # Connect bottom nav signals
        self.profile_screen.bottom_nav.tab_clicked.connect(self.nav_controller.on_tab_clicked)

        # Connect back button
        self.profile_screen.backClicked.connect(self.nav_controller.on_back_clicked)
        # Connect product click signal from HomeScreen's product grid for demonstration.
        # Optionally, if you have a bottom nav that emits tab clicked signals,
        # connect them to the navigation controller's on_tab_clicked:
        self.home_screen.bottom_nav.tab_clicked.connect(self.nav_controller.on_tab_clicked)
        self.cart_screen.bottom_nav.tab_clicked.connect(self.nav_controller.on_tab_clicked)


    def show_product_details(self, product_data: dict):
        """
        Slot to handle a product click.
        Creates a ProductDetailsScreen, connects its back signal,
        and adds it as a dynamic screen.
        """
        product_details_screen = ProductDetailsScreen(product_data)
        # Connect the back button signal to the controller's on_back_clicked slot.
        product_details_screen.backClicked.connect(self.nav_controller.on_back_clicked)
        self.nav_controller.add_screen("details", product_details_screen)



if __name__ == "__main__":
    # Create the QApplication instance
    app = QApplication(sys.argv)

    # Set a global font using the configuration settings (Inter with default size 24)
    default_font = QFont(SETTINGS["font_family"], SETTINGS["font_size_default"])
    # app.setFont(default_font)
    # logging.debug(
    #     f"Global application font set to {SETTINGS['font_family']} with size {SETTINGS['font_size_default']}.")

    # Create and show the main window
    window = MainWindow()
    window.show()
    logging.debug("Application started; MainWindow is now visible.")

    # Start the application event loop
    sys.exit(app.exec())
