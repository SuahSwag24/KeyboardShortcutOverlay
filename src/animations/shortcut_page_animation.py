from PyQt6.QtCore import QTimer, QPropertyAnimation, QEasingCurve
from PyQt6.QtWidgets import QGraphicsOpacityEffect

class ShortcutPageAnimation:
    FADE_DURATION   = 300
    PAGE_HOLD_MS    = 1500

    def __init__ (self, overlay):
        self.overlay = overlay
        self._timer = QTimer()
        self._timer.setSingleShot(True)
        self._timer.timeout.connect(self._on_hold_complete)

        self._effect = None
        self._active_anim = None

    def start(self):
        if getattr(self.overlay, '_total_pages', 1) <= 1:
            return
        
        self._schedule_next_page()

    def stop(self):
        self._timer.stop()
        if self._active_anim:
            self._active_anim.stop()
            self._active_anim = None

        self._clear_effect()

    def _schedule_next_page(self):
        self._timer.start(self.PAGE_HOLD_MS)

    def _on_hold_complete(self):
        self._fade_out(self._on_fade_out_complete)

    def _fade_out(self, callback):
        target = self.overlay.main_container
        effect = QGraphicsOpacityEffect(target)
        target.setGraphicsEffect(effect)
        self._effect = effect

        anim = QPropertyAnimation(effect, b"opacity")
        anim.setDuration(self.FADE_DURATION)
        anim.setStartValue(1.0)
        anim.setEndValue(0.0)
        anim.setEasingCurve(QEasingCurve.Type.OutQuad)
        anim.finished.connect(callback)
        self._active_anim = anim
        anim.start()

    def _on_fade_out_complete(self):
        self._clear_effect()
        next_page = (self.overlay._current_page + 1) % self.overlay._total_pages
        self.overlay._build_shortcut_list(self.overlay.current_modifier, page=next_page)
        self.overlay.main_container.setFixedHeight(self.overlay.current_static_height)
        self._fade_in(self._on_fade_in_complete)
    
    def _fade_in(self, callback):
        target = self.overlay.main_container

        effect = QGraphicsOpacityEffect(target)
        target.setGraphicsEffect(effect)
        self._effect = effect

        anim = QPropertyAnimation(effect, b"opacity")
        anim.setDuration(self.FADE_DURATION)
        anim.setStartValue(0.0)
        anim.setEndValue(1.0)
        anim.setEasingCurve(QEasingCurve.Type.InQuad)
        anim.finished.connect(callback)
        self._active_anim = anim
        anim.start()

    def _on_fade_in_complete(self):
        self._clear_effect()
        self._active_anim = None
        self._schedule_next_page()

    def _clear_effect(self):
        if self._effect:
            self.overlay.main_container.setGraphicsEffect(None)
            self._effect = None