from PyQt6.QtWidgets import QGraphicsOpacityEffect
from PyQt6.QtCore import QEasingCurve, QPropertyAnimation

class FlashShortcutAnimation:
    def __init__(self, overlay):
        self.overlay = overlay
        self.is_animating = False
        self.active_animations = []

    def flash_shortcut(self, combo, description=None):
        if self.active_animations:
            self._interrupt_current_animation()
            self.overlay._build_shortcut_list(self.overlay.current_modifier)
        
        self.is_animating = True
        target_row_label = None

        for i in range(self.overlay.shortcut_layout.count()):
            row_widget = self.overlay.shortcut_layout.itemAt(i).widget()
            
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

        self.overlay.main_container.setFixedHeight(self.overlay.current_static_height)
        self.overlay.show()
        self.overlay.title.setStyleSheet("color: transparent; padding: 10px 16px;")

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

        if hasattr(self.overlay, "current_modifier") and self.overlay.current_modifier:
            self.overlay.title.setStyleSheet("color: #ffffff; padding: 10px 16px;")
            self.overlay._build_shortcut_list(self.overlay.current_modifier)
            self.overlay.main_container.setFixedHeight(self.overlay.current_static_height)
            self.overlay.show()
        else:
            self.overlay.title.setStyleSheet("color: #ffffff; padding: 10px 16px;")
            self.overlay.hide()
            self.overlay.clear_shortcuts()

    def _interrupt_current_animation(self):
        for animation in self.active_animations:
            animation.stop()
        self.active_animations.clear()
        self.is_animating = False