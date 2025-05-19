# src/theme.py

DARK = {
    "bg": "#222220",
    "sidebar": "#2b2b29",
    "text": "#ffffff",
    "text_secondary": "#bdbdbd",
    "sidebar_divider": "#444444",
    "button": "#0078d4",
    "button_text": "#ffffff",
    "back_button": "#ff6058",
    "header": "#0078d4",
}
LIGHT = {
    "bg": "#ededec",
    "sidebar": "#bababa",
    "text": "#222222",
    "text_secondary": "#444444",
    "sidebar_divider": "#222222",  # heller für mehr Kontrast im Light Mode
    "button": "#0078d4",
    "button_text": "#ffffff",
    "back_button": "#ff6058",
    "header": "#0078d4",
}

def get_theme(mode):
    return DARK if mode == "dark" else LIGHT
