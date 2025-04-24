# config/settings.py
"""
General configuration settings for SmartBite.
This module aggregates color, font, and other application-wide settings.
"""

from config.colors import COLORS
from config.fonts import FONT_FAMILY, FONT_SIZE_DEFAULT, HEADING1_SIZE, HEADING2_SIZE, HEADING3_SIZE

# Debug mode flag (set True during development)
DEBUG = True

# Logging format (if needed in other parts of the app)
LOGGING_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

# You can add additional settings, e.g. API endpoints, here

# Global settings dictionary for convenient access
SETTINGS = {
    "colors": COLORS,
    "font_family": FONT_FAMILY,
    "font_size_default": FONT_SIZE_DEFAULT,
    "heading1_size": HEADING1_SIZE,
    "heading2_size": HEADING2_SIZE,
    "heading3_size": HEADING3_SIZE,
    "debug": DEBUG,
}
