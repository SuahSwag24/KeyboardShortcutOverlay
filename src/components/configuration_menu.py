from PyQt6.QtWidgets import QLabel, QSlider, QVBoxLayout, QWidget, QTabWidget
from PyQt6.QtCore import Qt, pyqtSignal
from config.settings import load_user_config, save_user_config

class GeneralConfigurations(QWidget):
    opacity_changed = pyqtSignal(float)
    text_opacity_changed = pyqtSignal(float)

    def __init__(self):
        super().__init__()

        config = load_user_config()

        layout = QVBoxLayout(self)

        opacity_label = QLabel("Overlay Opacity:")
        layout.addWidget(opacity_label)

        self.opacity_slider = QSlider(Qt.Orientation.Horizontal)
        self.opacity_slider.setRange(0, 100)
        self.opacity_slider.setValue(int(config.get("opacity", 0.3) * 100))
        self.opacity_slider.valueChanged.connect(self._on_opacity_change)
        layout.addWidget(self.opacity_slider)

        text_opacity_label = QLabel("Text Opacity:")
        layout.addWidget(text_opacity_label)

        self.text_opacity_slider = QSlider(Qt.Orientation.Horizontal)
        self.text_opacity_slider.setRange(0, 100)
        self.text_opacity_slider.setValue(int(config.get("text_opacity", 1.0) * 100))
        self.text_opacity_slider.valueChanged.connect(self._on_text_opacity_change)
        layout.addWidget(self.text_opacity_slider)

    def _on_opacity_change(self, value):
        opacity = value / 100.0
        config = load_user_config()
        config["opacity"] = opacity
        
        save_user_config(config)

        self.opacity_changed.emit(opacity)

    def _on_text_opacity_change(self, value):
        text_opacity = value / 100.0
        config = load_user_config()
        config["text_opacity"] = text_opacity

        save_user_config(config)

        self.text_opacity_changed.emit(text_opacity)


class ConfigurationWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Test")
        self.resize(400, 300)

        layout = QVBoxLayout()
        
        self.general_tab = GeneralConfigurations()
        layout.addWidget(self.general_tab)
        self.setLayout(layout)

    def show_window(self):
        self.show()
        self.raise_()
        self.activateWindow()