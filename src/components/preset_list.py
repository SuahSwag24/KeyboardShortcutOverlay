import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QListWidget,
    QPushButton, QInputDialog, QMessageBox
)

from utils.preset_util import SHORTCUT_LISTS_DIR

class PresetListPanel(QWidget):
    def __init__(self, on_select):
        super().__init__()
        self.on_select = on_select
        layout = QVBoxLayout(self)

        self.list_widget = QListWidget()
        self.list_widget.currentRowChanged.connect(self._on_row_changed)
        layout.addWidget(self.list_widget)

        btn_row = QHBoxLayout()
        self.add_btn = QPushButton("+ Add Preset")
        self.del_btn = QPushButton("Delete Preset")
        self.add_btn.clicked.connect(self._add_preset)
        self.del_btn.clicked.connect(self._delete_preset)
        btn_row.addWidget(self.add_btn)
        btn_row.addWidget(self.del_btn)
        layout.addLayout(btn_row)

        self.refresh()

    def refresh(self):
        self.list_widget.clear()
        self._paths = []

        for fname in sorted(os.listdir(SHORTCUT_LISTS_DIR)):
            if fname.endswith(".json"):
                self.list_widget.addItem(fname.replace(".json", ""))
                self._paths.append(os.path.join(SHORTCUT_LISTS_DIR, fname))

    def _on_row_changed(self, row):
        if 0 <= row < len(self._paths):
            self.on_select(self._paths[row])

    def _add_preset(self):
        name, ok = QInputDialog.getText(self, "New Preset", "Preset Name:")
        if ok and name.strip():
            path = os.path.join(SHORTCUT_LISTS_DIR, f"{name.strip()}.json")
            _save_preset(path, [])
            self.refresh()

    def _delete_preset(self):
        row = self.list_widget.currentRow()
        if row < 0:
            return
        
        path = self._paths[row]
        name = os.path.basename(path)
        confirm = QMessageBox.question(
            self, "Delete Preset",
            f"Delete '{name}' and all its app mappings?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirm == QMessageBox.StandardButton.Yes:
            os.remove(path)
            category = _load_category()
            updated = {exe: data for exe, data in category.items()
                       if not data.get("shortcut_file", "").endswith(name)}
            _save_category(updated)
            self.refresh()

