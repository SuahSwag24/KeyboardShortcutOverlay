from PyQt6.QtCore import QObject, pyqtSignal
from pynput import keyboard
import utils.shortcut_loader_utils as shortcut_loader
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
        self.listener = None
    
    def start(self):
        if self.listener:
            return

        self.listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release
        )
        self.listener.start()

    def stop(self):
        if not self.listener:
            return

        listener = self.listener
        self.listener = None
        listener.stop()
        self.reset_keys_pressed()

    def on_press(self, key):
        if not self.listener:
            return False

        canonical = self.listener.canonical(key)
        if canonical not in self.keys_pressed:
            self.keys_pressed.add(canonical)
            self.keys_changed.emit(self.keys_pressed)
            self.check_shortcuts_executed()

    def on_release(self, key):
        if not self.listener:
            return False
        
        self.keys_pressed.discard(self.listener.canonical(key))
        self.keys_changed.emit(self.keys_pressed)

    def check_shortcuts_executed(self):
        if not self.keys_pressed:
            return

        current_combo = format_keys(self.keys_pressed)
        description = shortcut_loader.SHORTCUTS_FLAT.get(current_combo, None)
        
        if description:
            self.shortcut_executed.emit(current_combo, description)

    def reset_keys_pressed(self):
        self.keys_pressed.clear()
        self.keys_changed.emit(self.keys_pressed)
            
