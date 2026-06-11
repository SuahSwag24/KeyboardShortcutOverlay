from PyQt6.QtWidgets import QHBoxLayout, QLabel, QSlider, QVBoxLayout, QWidget, QTabWidget
from PyQt6.QtCore import Qt, pyqtSignal
from config.settings import load_user_config, save_user_config

class GeneralConfigurations(QWidget):
    opacity_changed = pyqtSignal(float)
    text_opacity_changed = pyqtSignal(float)
    font_size_changed = pyqtSignal(int)
    list_item_count_changed = pyqtSignal(int)

    def __init__(self):
        super().__init__()

        config = load_user_config()

        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(12, 12, 12, 12)

        #   Overlay Opacity Option
        layout.addLayout(self._build_slider_option(
            "Overlay Opacity:",
            0,
            100,
            int(config.get("opacity", 0.3) * 100),
            "%",
            self._on_opacity_change,
            "opacity_slider",
            "opacity_value_label"    
        ))

        #   Text Opacity Option
        layout.addLayout(self._build_slider_option(
            "Text Overlay Opacity:",
            0,
            100,
            int(config.get("text_opacity", 0.3) * 100),
            "%",
            self._on_text_opacity_change,
            "text_opacity_slider",
            "text_opacity_value_label"    
        ))

        #   Font Size Option
        layout.addLayout(self._build_slider_option(
            "Font Size:",
            10,
            24,
            config.get("font_size", 14),
            "px",
            self._on_font_size_change,
            "font_size_slider",
            "font_size_value_label"    
        ))

        #   List Item Count Option
        layout.addLayout(self._build_slider_option(
            "List Item Count:",
            1,
            20,
            config.get("list_item_count", 10),
            " items",
            self._on_list_item_count_change,
            "list_item_count_slider",
            "list_item_count_value_label"    
        ))

    def _build_slider_option(self, label_text, min_val, max_val, initial_val, unit, callback, slider_attr, value_label_attr):
        slider_group = QVBoxLayout()
        slider_group.setSpacing(2)

        header = QHBoxLayout()
        header.addWidget(QLabel(label_text))
        header.addStretch()

        value_label = QLabel(f"{initial_val}{unit}")
        setattr(self, value_label_attr, value_label)
        header.addWidget(value_label)

        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setRange(min_val, max_val)
        slider.setValue(initial_val)
        slider.setFixedHeight(20)
        slider.valueChanged.connect(callback)
        setattr(self, slider_attr, slider)

        slider_group.addLayout(header)
        slider_group.addWidget(slider)
        return slider_group

    def _on_opacity_change(self, value):
        self.opacity_value_label.setText(f"{value}%")
        opacity = value / 100.0
        config = load_user_config()
        config["opacity"] = opacity
        
        save_user_config(config)

        self.opacity_changed.emit(opacity)

    def _on_text_opacity_change(self, value):
        self.text_opacity_value_label.setText(f"{value}%")
        text_opacity = value / 100.0
        config = load_user_config()
        config["text_opacity"] = text_opacity

        save_user_config(config)

        self.text_opacity_changed.emit(text_opacity)

    def _on_font_size_change(self, value):
        self.font_size_value_label.setText(f"{value}px")
        font_size = value
        config = load_user_config()
        config["font_size"] = font_size

        save_user_config(config)

        self.font_size_changed.emit(font_size)

    def _on_list_item_count_change(self, value):
        self.list_item_count_value_label.setText(f"{value} items")
        list_item_count = value
        config = load_user_config()
        config["list_item_count"] = list_item_count

        save_user_config(config)

        self.list_item_count_changed.emit(list_item_count)


class ConfigurationWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Test")
        self.resize(400, self.minimumHeight())

        layout = QVBoxLayout()
        
        self.general_tab = GeneralConfigurations()
        layout.addWidget(self.general_tab)
        self.setLayout(layout)

    def show_window(self):
        self.show()
        self.raise_()
        self.activateWindow()