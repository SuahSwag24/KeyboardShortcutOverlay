from PyQt6.QtWidgets import QHBoxLayout, QWidget, QLabel, QVBoxLayout, QSizePolicy
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QGuiApplication
from config.settings import MODIFIERS, SHORTCUT_ROW_HEIGHT, TITLE_HEIGHT, load_user_config
import utils.shortcut_loader_utils as shortcut_loader
from animations.flash_shortcut_animation import FlashShortcutAnimation
from animations.shortcut_page_animation import ShortcutPageAnimation
from utils.key_utils import normalize_modifiers, parse_combo

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
        self.pagination_animation = ShortcutPageAnimation(self)
        self.current_modifier = None

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.WindowDoesNotAcceptFocus |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.main_container = QWidget(self)
        self.main_container.setObjectName("main_container")
        self._apply_stylesheet()

        base_layout = QVBoxLayout(self)
        base_layout.setContentsMargins(0, 0, 0, 0)
        base_layout.addWidget(self.main_container)

        self.container_layout = QVBoxLayout(self.main_container)
        self.container_layout.setContentsMargins(0, 0, 0, 0)
        self.container_layout.setSpacing(0)
        self.container_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.title_widget = QWidget(self.main_container)
        self.title_widget.setFixedHeight(TITLE_HEIGHT)

        self.title_layout = QHBoxLayout(self.title_widget)
        self.title_layout.setContentsMargins(16, 10, 16, 10)
        self.title_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.container_layout.addWidget(self.title_widget)

        self.shortcut_layout = QVBoxLayout()
        self.shortcut_layout.setSpacing(8)
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
        
    def _build_shortcut_list(self, modifiers, page=0):
        self.clear_shortcuts()

        all_shortcuts = shortcut_loader.SHORTCUTS.get(modifiers, [])
        total = len(all_shortcuts)
        max_rows = self._list_item_count

        start = page * max_rows
        shortcuts = all_shortcuts[start : start + max_rows]
        self._total_pages = (total + max_rows - 1) // max_rows  # ceil division
        self._current_page = page

        while self.title_layout.count():
            item = self.title_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        modifier_keys = [getattr(m, 'name', str(m)).replace('Key.', '').strip() for m in modifiers]
        for mod in modifier_keys:
            mod_label = QLabel(f"{mod.capitalize()}")
            mod_label.setObjectName("key_block")
            self.title_layout.addWidget(mod_label)
            
        title_text = QLabel(" Shortcuts")
        title_text.setStyleSheet(f"color: rgba(255, 255, 255, {self._text_alpha}); font-size: {self._font_size}px; font-weight: bold; font-family: Segoe UI;")
        self.title_layout.addWidget(title_text)

        for combo, description in shortcuts:
            row_widget = QWidget()
            row_widget.setFixedHeight(SHORTCUT_ROW_HEIGHT)
            row_widget.setObjectName("row_widget")
            
            sp = row_widget.sizePolicy()
            sp.setRetainSizeWhenHidden(True)
            row_widget.setSizePolicy(sp)
            
            row_layout = QHBoxLayout(row_widget)
            row_layout.setContentsMargins(16, 0, 16, 0)

            keys = parse_combo(combo)

            for key in keys:
                if key.lower() in [m.lower() for m in modifier_keys]:
                    continue

                key_label = QLabel(f"{key}")
                key_label.setObjectName("key_block")
                key_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

                key_lower = key.lower()
                if key_lower in ['shift', 'ctrl', 'alt', 'cmd']:
                    key_label.setMinimumWidth(50)
                elif key_lower == 'space':
                    key_label.setMinimumWidth(80)
                else:
                    key_label.setMinimumWidth(30)

                row_layout.addWidget(key_label)

            desc_label = QLabel(description)
            desc_label.setObjectName("desc_label")
            desc_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

            row_layout.addWidget(desc_label)
            row_layout.addStretch()

            row_widget.setProperty("combo", combo)
            row_widget.setProperty("label_widget", row_widget)
            
            self.shortcut_layout.addWidget(row_widget)

        self.current_static_height = (len(shortcuts) * SHORTCUT_ROW_HEIGHT) + TITLE_HEIGHT + (max(0, len(shortcuts) - 1) * 8)
    
    def update_keys(self, keys_pressed):
        modifiers_held = frozenset(key for key in keys_pressed if key in MODIFIERS)
        self.current_modifier = normalize_modifiers(modifiers_held)

        if self.animation_manager.is_animating:
            return
        
        if keys_pressed and self.current_modifier:
            self.pagination_animation.stop()
            self._build_shortcut_list(self.current_modifier)
            self.main_container.setFixedHeight(self.current_static_height)
            self.adjustSize()
            self.position_window()
            self.show()
            self.pagination_animation.start()
        else:
            self.pagination_animation.stop()
            self.hide()

    def animate_execute(self, combo, description):
        self.pagination_animation.stop()
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
            QWidget#main_container{{
                background-color: rgba(30, 30, 30, {self._bg_alpha});
                border-radius: 12px;
            }}
            QLabel#title {{
                color: rgba(255, 255, 255, {self._text_alpha});
                font-size: {self._font_size}px;
                font-family: Segoe UI;
                font-weight: bold;
            }}
            QLabel#shortcut_layout{{
                font-size: {self._font_size}px;
                font-family: Segoe UI;
                font-weight: bold;
            }}
            QLabel#shortcut_label{{
                font-size: {self._font_size}px;
                font-family: Segoe UI;
                font-weight: bold;
            }}
            QLabel#key_block {{
                background-color: rgba(80, 80, 80, {self._bg_alpha});
                color: rgba(255, 255, 255, {self._text_alpha});
                border: 1px solid rgba(120, 120, 120, {self._bg_alpha});
                border-radius: 4px;
                padding: 2px 6px;
                font-size: {self._font_size}px;
                font-family: Segoe UI;
                font-weight: bold;
            }}
            QLabel#desc_label {{
                color: rgba(255, 255, 255, {self._text_alpha});
                font-size: {self._font_size}px;
                font-family: Segoe UI;
                padding-left: 8px;
            }}
        """)

    def find_page_for_combo(self, combo):
        all_shortcuts = shortcut_loader.SHORTCUTS.get(self.current_modifier, [])
        for i, (c, _) in enumerate(all_shortcuts):
            if c == combo:
                return i // self._list_item_count
        return 0