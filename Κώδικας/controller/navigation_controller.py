# controller/navigation_controller.py
import logging
from PyQt6.QtCore import QObject, pyqtSlot

class NavigationController(QObject):
    """
    Central controller that manages navigation between screens.
    There are two kinds of screens:
      1. Tab screens which are persistent and registered via register_screen.
         (e.g., Home, Search, Cart, Messages, Profile)
      2. Dynamic screens added via add_screen (e.g., Product Details).

    on_tab_clicked() handles switching between tab screens and logs which tab is highlighted.
    on_back_clicked() always routes back to the 'home' screen.
    """
    def __init__(self, stacked_widget, parent=None):
        super().__init__(parent)
        self.stacked_widget = stacked_widget
        # Registered tab screens; keys are screen names.
        self.tab_screens = {}
        logging.debug("NavigationController initialized with no tab screens.")

    def register_screen(self, name: str, widget):
        """
        Register a persistent (tab) screen by name.
        """
        logging.debug(f"register_screen(): Registering screen '{name}'.")
        self.tab_screens[name] = widget
        if self.stacked_widget.indexOf(widget) == -1:
            self.stacked_widget.addWidget(widget)
            logging.debug(f"register_screen(): Widget for screen '{name}' added to stacked_widget.")
        else:
            logging.debug(f"register_screen(): Widget for screen '{name}' already exists in stacked_widget.")
        logging.debug(f"register_screen(): Current registered screens: {list(self.tab_screens.keys())}.")

    @pyqtSlot(str)
    def on_tab_clicked(self, tab_name: str):
        """
        Switch to a registered tab screen when its name is clicked.
        Logs the highlighted tab and updates the bottom nav in the new screen if available.
        """
        logging.debug(f"on_tab_clicked(): Received request to switch to tab '{tab_name}'.")
        if tab_name in self.tab_screens:
            screen = self.tab_screens[tab_name]
            self.stacked_widget.setCurrentWidget(screen)
            logging.debug(f"on_tab_clicked(): Successfully switched to tab screen '{tab_name}'.")
            # Attempt to update the bottom navigation on the new screen
            if hasattr(screen, "bottom_nav"):
                screen.bottom_nav.current_tab = tab_name
                try:
                    screen.bottom_nav.update_selected_tab()
                    logging.debug(f"on_tab_clicked(): Bottom nav updated to highlight '{tab_name}'.")
                except Exception as e:
                    logging.error(f"on_tab_clicked(): Error updating bottom nav: {e}")
            else:
                logging.debug("on_tab_clicked(): Current screen does not have a 'bottom_nav' attribute.")
        else:
            logging.debug(f"on_tab_clicked(): No tab screen registered for '{tab_name}'.")

    def add_screen(self, screen_name: str, widget):
        """
        Adds a dynamic screen (e.g., product details) to the stacked widget and displays it.
        Dynamic screens are not kept in history since the back button always routes to home.
        """
        logging.debug(f"add_screen(): Adding dynamic screen '{screen_name}'.")
        self.stacked_widget.addWidget(widget)
        self.stacked_widget.setCurrentWidget(widget)
        logging.debug(f"add_screen(): Dynamic screen '{screen_name}' added and displayed.")

    @pyqtSlot()
    def on_back_clicked(self):
        """
        Handles back navigation.
        Always routes back to the registered 'home' screen and updates the bottom nav.
        """
        logging.debug("on_back_clicked(): Back button pressed; attempting to switch to 'home' screen.")
        if "home" in self.tab_screens:
            home_screen = self.tab_screens["home"]
            self.stacked_widget.setCurrentWidget(home_screen)
            logging.debug("on_back_clicked(): Successfully switched to 'home' screen.")
            # Update the bottom navigation on the home screen if available.
            if hasattr(home_screen, "bottom_nav"):
                home_screen.bottom_nav.current_tab = "home"
                try:
                    home_screen.bottom_nav.update_selected_tab()
                    logging.debug("on_back_clicked(): Home screen bottom nav updated to highlight 'home'.")
                except Exception as e:
                    logging.error(f"on_back_clicked(): Error updating home bottom nav: {e}")
            else:
                logging.debug("on_back_clicked(): Home screen does not have a 'bottom_nav' attribute.")
        else:
            logging.debug("on_back_clicked(): 'home' screen not registered.")

