from PyQt6.QtWidgets import QHBoxLayout, QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QGuiApplication
from config.settings import MODIFIERS, OVERLAY_ANCHOR_Y, OVERLAY_MARGIN_RIGHT, OVERLAY_WIDTH, SHORTCUT_ROW_HEIGHT, TITLE_HEIGHT
import utils.shortcut_loader_utils as shortcut_loader
from animations.flash_shortcut_animation import FlashShortcutAnimation
from utils.key_utils import normalize_modifiers

class Overlay(QWidget):
    def __init__(self):
        super().__init__()

        #   Overlay states
        self.animation_manager = FlashShortcutAnimation(self)
        self.current_modifier = None

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.WindowDoesNotAcceptFocus |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.main_container = QWidget(self)
        self.main_container.setStyleSheet("""
            QWidget {
                background-color: rgba(30, 30, 30, 180);
                border-radius: 12px;
            }
            QLabel {
                color: #ffffff;
                font-size: 14px;
                font-family: Segoe UI;
                font-weight: bold;   
            }
        """)

        base_layout = QVBoxLayout(self)
        base_layout.setContentsMargins(0, 0, 0, 0)
        base_layout.addWidget(self.main_container)

        self.container_layout = QVBoxLayout(self.main_container)
        self.container_layout.setContentsMargins(0, 0, 0, 0)
        self.container_layout.setSpacing(0)
        self.container_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.title = QLabel("Shortcut list:", self.main_container)
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setFixedHeight(TITLE_HEIGHT)
        self.title.setStyleSheet("padding: 10px 16px;")
        self.container_layout.addWidget(self.title)

        self.shortcut_layout = QVBoxLayout()
        self.shortcut_layout.setSpacing(0)
        self.shortcut_layout.setContentsMargins(0, 0, 0, 0)
        self.container_layout.addLayout(self.shortcut_layout)

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
        
    def _build_shortcut_list(self, modifiers):
        self.clear_shortcuts()
        shortcuts = shortcut_loader.SHORTCUTS.get(modifiers, [])

        if not shortcuts:
            label = QLabel(f"No shortcuts defined for this modifier.")
            label.setStyleSheet("padding: 10px 16px")
            self.shortcut_layout.addWidget(label)
            self.main_container.setFixedHeight(SHORTCUT_ROW_HEIGHT + TITLE_HEIGHT)
            self.show()

        for combo, description in shortcuts:
            row_widget = QWidget()
            row_widget.setFixedHeight(SHORTCUT_ROW_HEIGHT)

            row_layout = QHBoxLayout(row_widget)
            row_layout.setContentsMargins(16, 0, 16, 0)

            label = QLabel(f"{combo} -> {description}")
            label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

            row_widget.setProperty("combo", combo)
            row_widget.setProperty("label_widget", label)

            row_layout.addWidget(label)
            self.shortcut_layout.addWidget(row_widget)

        self.current_static_height = (len(shortcuts) * SHORTCUT_ROW_HEIGHT) + TITLE_HEIGHT
    
    def update_keys(self, keys_pressed):
        modifiers_held = frozenset(key for key in keys_pressed if key in MODIFIERS)
        self.current_modifier = normalize_modifiers(modifiers_held)

        if self.animation_manager.is_animating:
            return
        
        if keys_pressed and self.current_modifier:
            self._build_shortcut_list(self.current_modifier)
            self.main_container.setFixedHeight(self.current_static_height)
            self.title.setStyleSheet("color: #ffffff; padding: 10px 16px;")
            self.show()
        else:
            self.hide()

    def animate_execute(self, combo, description):
        self.animation_manager.flash_shortcut(combo, description)
        