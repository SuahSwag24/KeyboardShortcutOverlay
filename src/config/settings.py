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

#   Define special keys
SPECIAL_KEY_LABELS = {
    # Navigation
    "page_up":    "Page Up",
    "page_down":  "Page Down",
    "home":       "Home",
    "end":        "End",
    "insert":     "Insert",
    "delete":     "Delete",

    # Editing
    "enter":      "Enter",
    "backspace":  "Backspace",
    "space":      "Space",
    "tab":        "Tab",
    "caps_lock":  "Caps Lock",
    "esc":        "Esc",

    # Function keys
    "f1": "F1", "f2": "F2", "f3": "F3", "f4": "F4",
    "f5": "F5", "f6": "F6", "f7": "F7", "f8": "F8",
    "f9": "F9", "f10": "F10", "f11": "F11", "f12": "F12",

    # Numpad
    "num_lock":   "Num Lock",

    # Arrow keys
    "up":    "↑", "down": "↓", "left": "←", "right": "→",
    
    # Media / system
    "print_screen": "Print Screen",
    "scroll_lock":  "Scroll Lock",
    "pause":        "Pause",
}

VK_OEM_LABELS = {
    186: ";",   # VK_OEM_1
    187: "=",   # VK_OEM_PLUS
    188: ",",   # VK_OEM_COMMA
    189: "-",   # VK_OEM_MINUS
    190: ".",   # VK_OEM_PERIOD
    191: "/",   # VK_OEM_2
    192: "`",   # VK_OEM_3
    219: "[",   # VK_OEM_4
    220: "\\",  # VK_OEM_5
    221: "]",   # VK_OEM_6
    222: "'",   # VK_OEM_7
}