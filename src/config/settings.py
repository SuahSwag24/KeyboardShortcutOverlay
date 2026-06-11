import json, os
from pynput import keyboard

#   user_config.json loader
USER_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "user_config.json")

#   default configuration
defaults = {
    "opacity": 0.3,
    "text_opacity": 1.0,
    "font_size": 14,
    "list_item_count": 10
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
OVERLAY_WIDTH = 400
OVERLAY_MARGIN_RIGHT = 40
OVERLAY_ANCHOR_Y = 50
SHORTCUT_ROW_HEIGHT = 30
TITLE_HEIGHT = 40

#   Defining modifier keys in keycode
MODIFIERS = {
    keyboard.Key.ctrl_l, keyboard.Key.ctrl_r,
    keyboard.Key.alt_l, keyboard.Key.alt_r,
    keyboard.Key.shift_l, keyboard.Key.shift_r, keyboard.Key.shift,
    keyboard.Key.cmd
}

#   Mapping string representations to keycode for modifiers
MODIFIER_MAP = {
    "ctrl":  keyboard.Key.ctrl_l,
    "alt":   keyboard.Key.alt_l,
    "shift": keyboard.Key.shift_l,
    "cmd":   keyboard.Key.cmd
}

#   Normalize left and right modifiers to represent the same key for easier matching
MODIFIER_NORMALIZE = {
    keyboard.Key.ctrl_r: keyboard.Key.ctrl_l,
    keyboard.Key.alt_r: keyboard.Key.alt_l,
    keyboard.Key.shift_r : keyboard.Key.shift_l,
    keyboard.Key.shift : keyboard.Key.shift_l,
    keyboard.Key.cmd_l : keyboard.Key.cmd,
    keyboard.Key.cmd_r : keyboard.Key.cmd
}

#   Define order for displaying shortcuts in the overlay
KEY_ORDER = [
    "Ctrl", "Alt", "Shift", "Cmd", "Tab"
]