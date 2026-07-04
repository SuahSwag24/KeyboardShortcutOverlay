import json, os
from pynput import keyboard

from utils.path_util import get_config_dir
USER_CONFIG_PATH = os.path.join(get_config_dir(), "user_config.json")

#   default configuration
defaults = {
    "opacity": 0.3,
    "text_opacity": 1.0,
    "font_size": 14,
    "list_item_count": 10,
    "overlay_x_offset": 40,
    "overlay_y_offset": 50,
    "overlay_width": 400,
}

def load_user_config():
    try:
        with open(USER_CONFIG_PATH, 'r') as f:
            return {**defaults, **json.load(f)}
    except (FileNotFoundError, json.JSONDecodeError):
        return defaults

def save_user_config(config):
    try:
        with open(USER_CONFIG_PATH, 'w') as f:
            json.dump(config, f, indent=4)
    except (OSError, TypeError):
        pass

#   Overlay settings specifications
OVERLAY_HEIGHT = 300
SHORTCUT_ROW_HEIGHT = 30
TITLE_HEIGHT = 40

MODIFIERS = {
    keyboard.Key.ctrl,
    keyboard.Key.alt,
    keyboard.Key.shift,
    keyboard.Key.cmd
}

MODIFIER_MAP = {
    "ctrl":  keyboard.Key.ctrl,
    "alt":   keyboard.Key.alt,
    "shift": keyboard.Key.shift,
    "cmd":   keyboard.Key.cmd
}

#   Define order for displaying shortcuts in the overlay
KEY_ORDER = [
    "Ctrl", "Alt", "Shift", "Cmd", "Tab"
]

VK_OEM_LABELS = {
    # Function keys
    112: "F1",  113: "F2",  114: "F3",  115: "F4",
    116: "F5",  117: "F6",  118: "F7",  119: "F8",
    120: "F9",  121: "F10", 122: "F11", 123: "F12",

    # Navigation
    33: "Page Up", 34: "Page Down",
    35: "End",     36: "Home",
    45: "Insert",  46: "Delete",
    37: "←",       38: "↑",
    39: "→",       40: "↓",

    # Editing
    13: "Enter", 8: "Backspace", 27: "Esc",
    32: "Space", 9: "Tab",

    # Numpad
    96: "Num 0", 97: "Num 1", 98: "Num 2", 99: "Num 3",
    100: "Num 4", 101: "Num 5", 102: "Num 6", 103: "Num 7",
    104: "Num 8", 105: "Num 9",
    106: "Num *", 107: "Num +", 109: "Num -",
    110: "Num .", 111: "Num /",

    # OEM punctuation
    186: ";",   187: "=",  188: ",",  189: "-",
    190: ".",   191: "/",  192: "`",  219: "[",
    220: "\\",  221: "]",  222: "'",
}

APP_INFO = {
    "version_number": "1.2"
}

def get_app_info():
    return APP_INFO