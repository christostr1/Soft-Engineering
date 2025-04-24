# controller/navigation_controller.py
import logging
from PyQt6.QtCore import QObject, pyqtSlot


class NavigationController(QObject):
    """
    Central controller that manages navigation between screens.
    There are two kinds of screens:
      1. Tab screens which are persistent and registered via register_screen.
         (e.g., Home, Search)
      2. Dynamic screens added via add_screen (e.g., Product Details).

    on_tab_clicked() handles switching between tab screens.
    on_back_clicked() handles back navigation in the dynamic screen history.
    """

    def __init__(self, stacked_widget, parent=None):
        super().__init__(parent)
        self.stacked_widget = stacked_widget
        # History for dynamic screens (each entry is (screen_name, widget))
        self.history = []
        # Registered tab screens; keys are screen names
        self.tab_screens = {}

    def register_screen(self, name: str, widget):
        """Register a persistent (tab) screen by name."""
        self.tab_screens[name] = widget
        if self.stacked_widget.indexOf(widget) == -1:
            self.stacked_widget.addWidget(widget)
        logging.debug(f"Registered tab screen '{name}'.")

    @pyqtSlot(str)
    def on_tab_clicked(self, tab_name: str):
        """
        Switch to a registered tab screen when its name is clicked.
        """
        if tab_name in self.tab_screens:
            screen = self.tab_screens[tab_name]
            self.stacked_widget.setCurrentWidget(screen)
            logging.debug(f"Switched to tab screen '{tab_name}'.")
        else:
            logging.debug(f"No tab screen registered for '{tab_name}'.")

    def add_screen(self, screen_name: str, widget):
        """
        Adds a dynamic screen (e.g., product details) to the stacked widget,
        pushes it into history, and displays it.
        """
        self.history.append((screen_name, widget))
        self.stacked_widget.addWidget(widget)
        self.stacked_widget.setCurrentWidget(widget)
        logging.debug(f"Dynamic screen '{screen_name}' added and displayed.")

    @pyqtSlot()
    def on_back_clicked(self):
        """
        Handles back navigation for dynamic screens.
        Removes the current dynamic screen and displays the previous one.
        If there is no previous dynamic screen, it switches to a default tab (if available).
        """
        if len(self.history) > 1:
            # Remove current dynamic screen.
            current = self.history.pop()
            self.stacked_widget.removeWidget(current[1])
            # Show the previous dynamic screen.
            previous_screen = self.history[-1][1]
            self.stacked_widget.setCurrentWidget(previous_screen)
            logging.debug(f"Switched back to dynamic screen '{self.history[-1][0]}'.")
        else:
            # No dynamic screen history exists. Fallback to a default tab if registered.
            if "home" in self.tab_screens:
                self.stacked_widget.setCurrentWidget(self.tab_screens["home"])
                logging.debug("No dynamic screen in history. Switched to default 'home' screen.")
            else:
                logging.debug("No previous dynamic screen and no default 'home' registered.")
