from PyQt6.QtCore import QObject, pyqtSignal
from pynput import keyboard
from config.settings import MODIFIERS, SHORTCUTS, SHORTCUTS_FLAT
from utils.key_utils import format_keys, normalize_keys, normalize_modifiers

class KeySignalEmitter(QObject):
    #   Intiating Signals
    keys_changed = pyqtSignal(set)
    quit_app = pyqtSignal()
    shortcut_executed = pyqtSignal(str, str)

    #   Signal methods to detect key presses and releases
    def __init__(self):
        super().__init__()
        self.keys_pressed = set()
    
    def start(self):
        self.listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release
        )
        self.listener.start()

    def on_press(self, key):
        normalized = normalize_keys(key)
        if normalized not in self.keys_pressed:
            self.keys_pressed.add(normalized)
            self.keys_changed.emit(self.keys_pressed)
            self.check_shortcuts_executed()

    def on_release(self, key):
        if key == keyboard.Key.esc:
            self.quit_app.emit()
            return False
        
        self.keys_pressed.discard(normalize_keys(key))
        self.keys_changed.emit(self.keys_pressed)

    def check_shortcuts_executed(self):
        if not self.keys_pressed:
            return

        current_combo = format_keys(self.keys_pressed)
        description = SHORTCUTS_FLAT.get(current_combo, None)
        if description:
            self.shortcut_executed.emit(current_combo, description)
            