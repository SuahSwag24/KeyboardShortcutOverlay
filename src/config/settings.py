from pynput import keyboard
import json

#   Shortcut loader
def load_shortcuts(path="src/config/shortcuts.json"):
    with open(path, "r") as f:
        raw = json.load(f)

    shortcuts = {}
    for key_combo, actions in raw.items():
        keys = frozenset(MODIFIER_MAP[k] for k in key_combo.split("+"))
        shortcuts[keys] = [(a["combo"], a["description"]) for a in actions]

    return shortcuts

#   Overlay settings specifications
OVERLAY_WIDTH = 400
OVERLAY_MARGIN_RIGHT = 40
OVERLAY_ANCHOR_Y = 400
SHORTCUT_ROW_HEIGHT = 40
TITLE_HEIGHT = 40

#   Defining modifier keys in keycode
MODIFIERS = {
    keyboard.Key.ctrl_l, keyboard.Key.ctrl_r,
    keyboard.Key.alt_l, keyboard.Key.alt_r,
    keyboard.Key.shift_l, keyboard.Key.shift_r,
    keyboard.Key.cmd
}

#   Mapping string representations to keycode for modifiers
MODIFIER_MAP = {
    "ctrl":  keyboard.Key.ctrl_l,
    "alt":   keyboard.Key.alt_l,
    "shift": keyboard.Key.shift_l,
    "cmd":   keyboard.Key.cmd,
}

#   Normalize left and right modifiers to represent the same key for easier matching
MODIFIER_NORMALIZE = {
    keyboard.Key.ctrl_r: keyboard.Key.ctrl_l,
    keyboard.Key.alt_r: keyboard.Key.alt_l,
    keyboard.Key.shift_r: keyboard.Key.shift_l,
}

#   Define order for displaying shortcuts in the overlay
KEY_ORDER = [
    "Ctrl", "Alt", "Shift", "Win"
]

#   Establish shortcut JSON into program
SHORTCUTS = load_shortcuts()