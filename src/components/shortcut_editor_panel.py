from PyQt6.QtWidgets import (
    QDialog, QHeaderView, QTableWidget, QTableWidgetItem, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QInputDialog,
)
from utils.preset_util import _load_preset, _save_preset
from components.shortcut_recorder import ShortcutRecorderDialog
import utils.shortcut_loader_utils as shortcut_loader

class ShortcutEditorPanel(QWidget):
    def __init__(self, emitter, on_shortcuts_changed=None):
        super().__init__()
        self.emitter = emitter
        self._current_path = None
        self.on_shortcuts_changed = on_shortcuts_changed

        layout = QVBoxLayout(self)

        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Combo", "Modifier", "Description"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setEditTriggers(QTableWidget.EditTrigger.DoubleClicked)
        self.table.itemChanged.connect(self._on_item_changed)
        layout.addWidget(self.table)

        btn_row = QHBoxLayout()
        self.add_btn    = QPushButton("+ Add Shortcut")
        self.delete_btn = QPushButton("Delete")
        self.add_btn.clicked.connect(self._add_shortcut)
        self.delete_btn.clicked.connect(self._delete_shortcut)
        btn_row.addWidget(self.add_btn)
        btn_row.addWidget(self.delete_btn)
        layout.addLayout(btn_row)

    def load_preset(self, path):
        self._current_path = path
        self._refresh_table(_load_preset(path))

    def _refresh_table(self, data):
        self.table.blockSignals(True)
        self.table.setRowCount(0)
        for entry in data:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(entry["combo"]))
            self.table.setItem(row, 1, QTableWidgetItem(entry["modifier"]))
            self.table.setItem(row, 2, QTableWidgetItem(entry["description"]))
        self.table.blockSignals(False)

    def _notify_change(self):
        if callable(self.on_shortcuts_changed):
            self.on_shortcuts_changed()

    def _on_item_changed(self, _item):
        self._save_current()

    def _add_shortcut(self):
        if not self._current_path:
            return
        
        dlg = ShortcutRecorderDialog(self.emitter, self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            modifier, combo = dlg.get_result()
            desc, ok = QInputDialog.getText(self, "Description", "Shortcut description:")
            if ok and desc.strip():
                data = _load_preset(self._current_path)
                data.append({"modifier": modifier, "combo": combo, "description": desc.strip()})
                _save_preset(self._current_path, data)
                shortcut_loader.load_context_shortcuts(self._current_path)
                self._refresh_table(data)
                self._notify_change()

    def _delete_shortcut(self):
        row = self.table.currentRow()
        if row < 0 or not self._current_path:
            return
        data = _load_preset(self._current_path)
        data.pop(row)
        _save_preset(self._current_path, data)
        shortcut_loader.load_context_shortcuts(self._current_path)
        self._refresh_table(data)
        self._notify_change()

    def _save_current(self):
        if not self._current_path:
            return
        data = []
        for r in range(self.table.rowCount()):
            data.append({
                "combo":       self.table.item(r, 0).text() if self.table.item(r, 0) else "",
                "modifier":    self.table.item(r, 1).text() if self.table.item(r, 1) else "",
                "description": self.table.item(r, 2).text() if self.table.item(r, 2) else "",
            })
        _save_preset(self._current_path, data)
        shortcut_loader.load_context_shortcuts(self._current_path)
        self._notify_change()