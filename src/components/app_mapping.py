import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QListWidget,
    QPushButton, QInputDialog, QFileDialog, QLabel
)

from utils.preset_util import _load_category, _save_category

class AppMappingPanel(QWidget):
    def __init__(self):
        super().__init__()
        self._current_preset_path = None
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Mapped Applications:"))

        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)

        btn_row = QHBoxLayout()
        self.add_btn = QPushButton("+ Add App")
        self.del_btn = QPushButton("Remove")
        self.add_btn.clicked.connect(self._add_app)
        self.del_btn.clicked.connect(self._remove_app)
        btn_row.addWidget(self.add_btn)
        btn_row.addWidget(self.del_btn)
        layout.addLayout(btn_row)

    def load_preset(self, preset_path):
        self._current_preset_path = preset_path
        self._refresh()

    def _refresh(self):
        self.list_widget.clear()
        if not self._current_preset_path:
            return
        category = _load_category()
        preset_fname = os.path.basename(self._current_preset_path)
        for exe, data in category.items():
            if data.get("shortcut_file", "").endswith(preset_fname):
                self.list_widget.addItem(f"{exe}  ({data.get('application_name', '')})")
        self._exes = [
            exe for exe, data in category.items()
            if data.get("shortcut_file", "").endswith(preset_fname)
        ]

    def _add_app(self):
        if not self._current_preset_path:
            return
        exe_path, _ = QFileDialog.getOpenFileName(
            self, "Select Application", "C:/", "Executables (*.exe)"
        )
        if not exe_path:
            return
        exe_name = os.path.basename(exe_path)

        app_label, ok1 = QInputDialog.getText(self, "App Name", "Display name:")
        category_str, ok2 = QInputDialog.getText(self, "Category", "Category (e.g. development):")
        if not (ok1 and ok2):
            return

        preset_rel = (
            "KeyboardShortcutOverlay/src/config/shortcut_lists/"
            + os.path.basename(self._current_preset_path)
        )
        cat_data = _load_category()
        cat_data[exe_name] = {
            "application_name": app_label.strip(),
            "category": category_str.strip(),
            "shortcut_file": preset_rel
        }
        _save_category(cat_data)
        self._refresh()

    def _remove_app(self):
        row = self.list_widget.currentRow()
        if row < 0 or row >= len(self._exes):
            return
        exe = self._exes[row]
        cat_data = _load_category()
        cat_data.pop(exe, None)
        _save_category(cat_data)
        self._refresh()