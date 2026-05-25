from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QGuiApplication
from utils.key_utils import format_keys, normalize_modifiers
from config.settings import MODIFIER_NORMALIZE, MODIFIERS, OVERLAY_ANCHOR_Y, OVERLAY_MARGIN_RIGHT, OVERLAY_WIDTH, SHORTCUTS, TITLE_HEIGHT, SHORTCUT_ROW_HEIGHT


class Overlay(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlags (
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.WindowDoesNotAcceptFocus |
            Qt.WindowType.Tool
        )

        self.setStyleSheet ("""
            QWidget {
                background-color: rgba(30, 30, 30, 180);
                border-radius: 12px;
            }
            
            QLabel {
                color: #ffffff;
                font-size: 14px;
                font-family: Segoe UI;
                padding: 10px 16px;
                font-weight: bold;   
            }
        """)

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        title = QLabel("Current Keys Pressed:")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFixedHeight(TITLE_HEIGHT)

        self.shortcut_layout = QVBoxLayout()
        self.shortcut_layout.setSpacing(2)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        layout.addWidget(title)
        layout.addLayout(self.shortcut_layout)

        self.setLayout(layout)
        self.position_window()
        self.setFixedWidth(OVERLAY_WIDTH)

    def position_window(self):
        screen_geometry = QGuiApplication.primaryScreen().geometry()
        x = screen_geometry.width() - self.width() - OVERLAY_MARGIN_RIGHT
        y = OVERLAY_ANCHOR_Y
        self.move(x, y)

    def showEvent(self, event):
        self.position_window()
        super().showEvent(event)

    def clear_shortcuts(self):
        while self.shortcut_layout.count():
            item = self.shortcut_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
    
    def update_keys(self, keys_pressed):
        if keys_pressed:
            modifiers_held = frozenset(key for key in keys_pressed if key in MODIFIERS)
            modifiers_held = normalize_modifiers(modifiers_held)
            if modifiers_held:
                shortcuts = SHORTCUTS.get(modifiers_held, None)
                self.clear_shortcuts()
                if shortcuts:
                    for combo, description in shortcuts:
                        label = QLabel(f"{combo} -> {description}")
                        label.setFixedHeight(40)
                        self.shortcut_layout.addWidget(label)
                    self.show()
                else:
                    label = QLabel(f"No shortcuts defined for this modiifer.")
                    self.shortcut_layout.addWidget(label)
                    self.show()
            else:
                self.hide()
        else:
            self.hide()
