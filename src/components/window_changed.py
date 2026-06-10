from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QGuiApplication
from utils.shortcut_loader_utils import get_shortcut_path, load_context_shortcuts, reset_to_global
from config.settings import OVERLAY_WIDTH, OVERLAY_MARGIN_RIGHT

NOTIF_HEIGHT = 52
NOTIF_ANCHOR_Y = 10  # distance from top of screen

class WindowChangeNotification(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.WindowDoesNotAcceptFocus |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowOpacity(0.0)

        self.container = QWidget(self)
        self.container.setStyleSheet("""
            QWidget {
                background-color: rgba(30, 30, 30, 200);
                border-radius: 10px;
            }
        """)

        layout = QVBoxLayout(self.container)
        layout.setContentsMargins(16, 10, 16, 10)

        self.label = QLabel("", self.container)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("""
            color: #cccccc;
            font-size: 13px;
            font-family: Segoe UI;
            font-weight: normal;
            background: transparent;
        """)
        layout.addWidget(self.label)

        self._hide_timer = QTimer(self)
        self._hide_timer.setSingleShot(True)
        self._hide_timer.timeout.connect(self._fade_out)

        self._fade_in_anim = QPropertyAnimation(self, b"windowOpacity")
        self._fade_in_anim.setDuration(180)
        self._fade_in_anim.setEasingCurve(QEasingCurve.Type.OutCubic)

        self._fade_out_anim = QPropertyAnimation(self, b"windowOpacity")
        self._fade_out_anim.setDuration(350)
        self._fade_out_anim.setEasingCurve(QEasingCurve.Type.InCubic)
        self._fade_out_anim.finished.connect(self.hide)

    def _position(self):
        screen = QGuiApplication.primaryScreen().geometry()
        x = screen.width() - self.width() - OVERLAY_MARGIN_RIGHT
        self.move(x, NOTIF_ANCHOR_Y)

    def notify(self, window_title, executable, display_ms=1000):
        self.on_window_changed(executable)

        self.label.setText(f"{executable}")

        self.label.adjustSize()
        label_w = self.label.sizeHint().width()
        label_h = self.label.sizeHint().height()

        h_padding, v_padding = 32, 20
        new_w = label_w + h_padding
        new_h = label_h + v_padding

        self.container.setFixedSize(new_w, new_h)
        self.setFixedSize(new_w, new_h)

        self._position()
        self._hide_timer.stop()
        self._fade_out_anim.stop()

        self.setWindowOpacity(0.0)
        self.show()

        self._fade_in_anim.setStartValue(0.0)
        self._fade_in_anim.setEndValue(1.0)
        self._fade_in_anim.start()

        self._hide_timer.start(display_ms)

    def _fade_out(self):
        self._fade_out_anim.setStartValue(self.windowOpacity())
        self._fade_out_anim.setEndValue(0.0)
        self._fade_out_anim.start()

    def on_window_changed(self, executable):
        shortcut_path = get_shortcut_path(executable)

        if shortcut_path:
            load_context_shortcuts(shortcut_path)
        else:
            reset_to_global()