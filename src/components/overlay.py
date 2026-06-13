from PyQt6.QtWidgets import QHBoxLayout, QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFontMetrics, QGuiApplication
from config.settings import MODIFIERS, SHORTCUT_ROW_HEIGHT, TITLE_HEIGHT, load_user_config
import utils.shortcut_loader_utils as shortcut_loader
from animations.flash_shortcut_animation import FlashShortcutAnimation
from utils.key_utils import normalize_modifiers

class Overlay(QWidget):
    def __init__(self):
        super().__init__()

        config = load_user_config()
        self._bg_alpha = int(config.get("opacity", 0.3) * 255)
        self._text_alpha = int(config.get("text_opacity", 1.0) * 255)
        self._font_size = config.get("font_size", 14)
        self._list_item_count = config.get("list_item_count", 10)
        self._overlay_width = config.get("overlay_width", 400)
        self._overlay_x_offset = config.get("overlay_x_offset", 40)
        self._overlay_y_offset = config.get("overlay_y_offset", 50)

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
        self.main_container.setStyleSheet(f"""
            QWidget {{
                background-color: rgba(30, 30, 30, {self._bg_alpha});
                border-radius: 12px;
            }}
            QLabel {{
                color: rgba(255, 255, 255, {self._text_alpha});
                font-size: {self._font_size}px;
                font-family: Segoe UI;
                font-weight: bold;   
            }}
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

        self.setFixedWidth(self._overlay_width)

    def position_window(self):
        screen_geometry = QGuiApplication.primaryScreen().geometry()
        x = screen_geometry.width() - self.width() - self._overlay_x_offset
        y = self._overlay_y_offset
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
        shortcuts = shortcuts[:self._list_item_count]

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

            full_text = f"{combo} -> {description}"
            fm = QFontMetrics(self.font())
            available_width = self._overlay_width - 32
            elided = fm.elidedText(full_text, Qt.TextElideMode.ElideRight, available_width)
            label = QLabel(elided)

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

    def set_opacity(self, value: float):
        self._bg_alpha = int(value * 255)
        self._apply_stylesheet()

    def set_text_opacity(self, value: float):
        self._text_alpha = int(value * 255)
        self._apply_stylesheet()

    def set_font_size(self, value: int):
        self._font_size = value
        self._apply_stylesheet()

    def set_list_item_count(self, value: int):
        self._list_item_count = value

    def set_overlay_width(self, value: int):
        self._overlay_width = value
        self.setFixedWidth(value)
        self.position_window()

    def set_overlay_x_offset(self, value: int):
        self._overlay_x_offset = value
        self.position_window()

    def set_overlay_y_offset(self, value: int):
        self._overlay_y_offset = value
        self.position_window()      

    def _apply_stylesheet(self):
        self.main_container.setStyleSheet(f"""
            QWidget {{
                background-color: rgba(30, 30, 30, {self._bg_alpha});
                border-radius: 12px;
            }}
            QLabel {{
                color: rgba(255, 255, 255, {self._text_alpha});
                font-size: {self._font_size}px;
                font-family: Segoe UI;
                font-weight: bold;
            }}
        """)