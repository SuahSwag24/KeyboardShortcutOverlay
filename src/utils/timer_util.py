from PyQt6.QtCore import QObject, QTimer, pyqtSignal
from components.window_focus_listener import get_focused_window

class BackgroundTimerUtil(QObject):
    window_changed = pyqtSignal(str, str)

    def __init__(self, interval_ms, parent=None):
        super().__init__(parent)
        self.last_hwnd = None

        self.focus_timer = QTimer(self)
        self.focus_timer.setInterval(interval_ms)

        self.focus_timer.timeout.connect(self._check_focused_window)

    def start_all(self):
        self.focus_timer.start()

    def _check_focused_window(self):
        hwnd, window_title, executable = get_focused_window()
        if hwnd and hwnd != self.last_hwnd:
            self.last_hwnd = hwnd
            if window_title:
                self.window_changed.emit(window_title, executable)