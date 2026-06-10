from pynput import keyboard

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