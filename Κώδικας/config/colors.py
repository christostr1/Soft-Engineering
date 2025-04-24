# config/colors.py
"""
Colors configuration for SmartBite.
This module defines placeholder colors for five categories – Primary, Secondary, Success,
Error, and Info – with each category containing six subcategories:
    - Main
    - Surface
    - Border
    - Hover
    - Pressed
    - Focus
"""

PRIMARY = {
    "main": "#4C4DDC",
    "surface": "#F5F5FF",
    "border": "#DFE0F3",
    "hover": "#fe8c00",
    "pressed": "#085885",
    "focus": "#DBDBF8"
}

SECONDARY = {
    "main": "#FFD33C",
    "surface": "#FFF6D8",
    "border": "#FFF0BE",
    "hover": "#D5B032",
    "pressed": "#806A1E",
    "focus": "#FFF6D8"
}

SUCCESS = {
    "main": "#50CD89",
    "surface": "#F2FFF8",
    "border": "#C5EED8",
    "hover": "#46B277",
    "pressed": "#28593F",
    "focus": "#DCF5E7"
}

ERROR = {
    "main": "#F14141",
    "surface": "#FFF2F2",
    "border": "#FAC0C0",
    "hover": "#D93A3A",
    "pressed": "#802A2A",
    "focus": "#FCD9D9"
}

INFO = {
    "main": "#7239EA",
    "surface": "#F6F2FF",
    "border": "#D0BDF8",
    "hover": "#6633D1",
    "pressed": "#3F2478",
    "focus": "#E3D7FB"
}

NEUTRAL = {
    "Neutral 10": "#FFFFFF",
    "Neutral 20": "#F5F5F5",
    "Neutral 30": "#EDEDED",
    "Neutral 40": "#D6D6D6",
    "Neutral 50": "#C2C2C2",
    "Neutral 60": "#878787",
    "Neutral 70": "#606060",
    "Neutral 80": "#383838",
    "Neutral 90": "#403A3A",
    "Neutral 100": "#101010",
}

# A dictionary combining all the colors for easy access
COLORS = {
    "primary": PRIMARY,
    "secondary": SECONDARY,
    "success": SUCCESS,
    "error": ERROR,
    "info": INFO,
    "neutral": NEUTRAL,
}
