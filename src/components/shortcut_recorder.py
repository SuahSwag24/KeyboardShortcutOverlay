from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QDialogButtonBox
from PyQt6.QtCore import Qt
from pynput import keyboard
    
class ShortcutRecorderDialog(QDialog):
    def __init__(self, emitter, parent=None):
        super().__init__(parent)
        self.emitter = emitter
        self.setWindowTitle("Record Shortcut")
        self.setModal(True)
        self.resize(300, 120)

        self._captured_keys = set()
        self._combo_str = ""
        self._modifier_str = ""
        self._listener = None
        self._was_emitter_running = False
        self._is_finished = False

        layout = QVBoxLayout(self)
        self.prompt = QLabel("Press your key combinations...")
        self.prompt.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.display = QLabel("")
        self.display.setAlignment(Qt.AlignmentFlag.AlignCenter)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(self.prompt)
        layout.addWidget(self.display)
        layout.addWidget(buttons)

    def showEvent(self, event):
        super().showEvent(event)

        self._was_emitter_running = bool(
            self.emitter and getattr(self.emitter, "listener", None)
        )
        if self._was_emitter_running:
            self.emitter.stop()
        
        self._start_recording()

    def closeEvent(self, event):
        self._finish_recording()
        super().closeEvent(event)

    def done(self, result):
        self._finish_recording()
        super().done(result)

    def _finish_recording(self):
        if self._is_finished:
            return

        self._is_finished = True
        self._stop_recording()

        if self._was_emitter_running and self.emitter:
            self.emitter.start()

    def _start_recording(self):
        self._listener = keyboard.Listener(
            on_press=self._on_press,
            on_release=self._on_release
        )
        self._listener.start()

    def _stop_recording(self):
        if self._listener:
            self._listener.stop()
            self._listener = None

    def _on_press(self, key):
        canonical = self._listener.canonical(key)
        self._captured_keys.add(canonical)
        self._update_display()

    def _on_release(self, key):
        if self._listener:
            self._captured_keys.discard(self._listener.canonical(key))

    def _update_display(self):
        from utils.key_utils import format_keys

        self._combo_str = format_keys(self._captured_keys)

        modifier_keys = {"ctrl", "alt", "shift", "cmd"}
        parts = [p.lower() for p in self._combo_str.split(" + ")
                 if p.lower() in modifier_keys]
        self._modifier_str = "+".join(parts) if parts else "ctrl"

        from PyQt6.QtCore import QMetaObject, Qt
        self.display.setText(self._combo_str)

    def get_result(self):
        return self._modifier_str, self._combo_str