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

        target_page = self.overlay.find_page_for_combo(combo)
        self.overlay._build_shortcut_list(self.overlay.current_modifier, page=target_page)
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
                        label_widget.setVisible(True)
                    else:
                        label_widget.setVisible(False)

        self.overlay.main_container.setFixedHeight(self.overlay.current_static_height)
        self.overlay.show()

        if target_row_label:
            self.animate_row_fade(target_row_label)
        else:
            self._on_fade_complete()

    def animate_row_fade(self, label_widget):
        effect = QGraphicsOpacityEffect(label_widget)
        label_widget.setGraphicsEffect(effect)

        animation = QPropertyAnimation(effect, b"opacity")
        animation.setDuration(800)
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
            self.overlay._build_shortcut_list(self.overlay.current_modifier)
            self.overlay.main_container.setFixedHeight(self.overlay.current_static_height)
            self.overlay.show()
            self.overlay.pagination_animation.start()
        else:
            self.overlay.hide()
            self.overlay.clear_shortcuts()

    def _interrupt_current_animation(self):
        for animation in self.active_animations:
            animation.stop()
        self.active_animations.clear()
        self.is_animating = False