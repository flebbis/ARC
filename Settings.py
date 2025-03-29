import json
from ScreenRes import ScreenRes

SETTINGS_FILE = "program_settings.json"

def load_settings():
    """Laddar programinställningar från JSON-filen och sparar standardupplösningen om den saknas."""
    try:
        with open(SETTINGS_FILE, "r") as f:
            settings = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        settings = {}

    if "default" not in settings:
        width, height = ScreenRes.get()
        settings["default"] = {
            "resolution": [width, height],
            "fps": ScreenRes.get_max_fps()
        }
        save_settings(settings)

    return settings

def save_settings(settings):
    """Sparar programinställningar till JSON-filen."""
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)