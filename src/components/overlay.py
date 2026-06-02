from PyQt6.QtWidgets import QApplication, QGraphicsOpacityEffect, QHBoxLayout, QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import QEasingCurve, QPropertyAnimation, Qt
from PyQt6.QtGui import QGuiApplication
from utils.key_utils import format_keys, normalize_modifiers
from config.settings import MODIFIER_NORMALIZE, MODIFIERS, OVERLAY_ANCHOR_Y, OVERLAY_MARGIN_RIGHT, OVERLAY_WIDTH, SHORTCUTS, TITLE_HEIGHT, SHORTCUT_ROW_HEIGHT


class Overlay(QWidget):
    def __init__(self):
        super().__init__()

        #   Overlay states
        self.is_animating = False
        self.active_animations = []

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
    
    def update_keys(self, keys_pressed):
        if self.is_animating:
            return

        if keys_pressed:
            modifiers_held = frozenset(key for key in keys_pressed if key in MODIFIERS)
            modifiers_held = normalize_modifiers(modifiers_held)

            if modifiers_held:
                shortcuts = SHORTCUTS.get(modifiers_held, None)
                self.clear_shortcuts()

                if shortcuts:
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
                    self.main_container.setFixedHeight(self.current_static_height)
                    self.show()
                else:
                    label = QLabel(f"No shortcuts defined for this modiifer.")
                    label.setStyleSheet("padding: 10px 16px")
                    self.shortcut_layout.addWidget(label)
                    self.main_container.setFixedHeight(SHORTCUT_ROW_HEIGHT + TITLE_HEIGHT)
                    self.show()
            else:
                self.hide()
        else:
            self.hide()

    def flash_shortcut(self, combo, description):
        if self.active_animations:
            self._interrupt_current_animation()

        self.is_animating = True
        target_row_label = None

        for i in range(self.shortcut_layout.count()):
            row_widget = self.shortcut_layout.itemAt(i).widget()
            if row_widget:
                label_widget = row_widget.property("label_widget")
                row_combo = row_widget.property("combo")

                if label_widget:
                    label_widget.setGraphicsEffect(None)

                    if row_combo == combo:
                        target_row_label = label_widget
                        label_widget.setStyleSheet("color: #ffffff;") 
                    else:
                        label_widget.setStyleSheet("color: transparent;")

        self.main_container.setFixedHeight(self.current_static_height)
        self.show()
        self.title.setStyleSheet("color: transparent; padding: 10px 16px;")

        if target_row_label:
            self.animate_row_fade(target_row_label)
        else:
            self._on_fade_complete()

    def animate_row_fade(self, label_widget):
        effect = QGraphicsOpacityEffect(label_widget)
        label_widget.setGraphicsEffect(effect)

        animation = QPropertyAnimation(effect, b"opacity")
        animation.setDuration(1500)
        animation.setStartValue(1.0)
        animation.setEndValue(0.0)
        animation.setEasingCurve(QEasingCurve.Type.OutQuad)

        animation.finished.connect(self._on_fade_complete)
        self.active_animations.append(animation)
        animation.start()

    def _on_fade_complete(self):
        self.is_animating = False
        self.active_animations.clear()

        self.title.setStyleSheet("color: #ffffff; padding: 10px 16px;")
        self.hide()
        self.clear_shortcuts()

    def _interrupt_current_animation(self):
        for animation in self.active_animations:
            animation.stop()
        self.active_animations.clear()
        self.is_animating = False
        