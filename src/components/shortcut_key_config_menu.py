import json, os
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QDialogButtonBox
from PyQt6.QtCore import Qt
from pynput import keyboard
from config.settings import SPECIAL_KEY_LABELS, VK_OEM_LABELS, KEY_ORDER, MODIFIERS

SHORTCUT_LISTS_DIR = os.path.join(os.path.dirname(__file__), "..", "config", "shortcut_lists")
CATEGORY_PATH = os.path.join(os.path.dirname(__file__), "..", "config", "application_category.json")

#   Load preset JSON into lists
def _load_preset(path):
    with open(path, "r") as f:
        return json.load(f)
    
#   Save list of shortcut to JSON
def _save_preset(path, new_data):
    with open(path, "w") as f:
        json.dump(new_data, f, indent=2)

def _load_category():
    with open(CATEGORY_PATH, "r") as f:
        return json.load(f)
    
def _save_category(new_data):
    with open(CATEGORY_PATH, "w") as f:
        return json.dump(new_data, f, indent=4)
    
class ShortcutRecorderDialog(QDialog):
    def __init__(self, emitter, parent=None):
        super().__init__(parent)
        self.emitter = emitter
        self.setWindowTitle("Record Shortcut")
        self.setModal(True)
        self.resize(300, 120)

        self._captured_keys = set()
        self._combo_str = ""
        self._modifier_str = ""
        self._listener = None
        self._was_emitter_running = False
        self._is_finished = False

        layout = QVBoxLayout(self)
        self.prompt = QLabel("Press your key combinations...")
        self.prompt.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.display = QLabel("")
        self.display.setAlignment(Qt.AlignmentFlag.AlignCenter)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(self.prompt)
        layout.addWidget(self.display)
        layout.addWidget(buttons)

    def showEvent(self, event):
        super().showEvent(event)

        self._was_emitter_running = bool(
            self.emitter and getattr(self.emitter, "listener", None)
        )
        if self._was_emitter_running:
            self.emitter.stop()
        
        self._start_recording()

    def closeEvent(self, event):
        self._finish_recording()
        super().closeEvent(event)

    def done(self, result):
        self._finish_recording()
        super().done(result)

    def _finish_recording(self):
        if self._is_finished:
            return

        self._is_finished = True
        self._stop_recording()

        if self._was_emitter_running and self.emitter:
            self.emitter.start()

    def _start_recording(self):
        self._listener = keyboard.Listener(
            on_press=self._on_press,
            on_release=self._on_release
        )
        self._listener.start()

    def _stop_recording(self):
        if self._listener:
            self._listener.stop()
            self._listener = None

    def _on_press(self, key):
        canonical = self._listener.canonical(key)
        self._captured_keys.add(canonical)
        self._update_display()

    def _on_release(self, key):
        self._update_display()

    def _update_display(self):
        from utils.key_utils import format_keys

        self._combo_str = format_keys(self._captured_keys)

        modifier_keys = MODIFIERS
        parts = [p.lower() for p in self._combo_str.split(" + ")
                 if p.lower() in modifier_keys]
        self._modifier_str = "+".join(parts) if parts else "ctrl"

        from PyQt6.QtCore import QMetaObject, Qt
        self.display.setText(self._combo_str)

    def get_result(self):
        return self._modifier_str, self._combo_str
    

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QListWidget,
    QPushButton, QInputDialog, QMessageBox
)

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

from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView

class ShortcutEditorPanel(QWidget):
    def __init__(self, emitter):
        super().__init__()
        self.emitter = emitter
        self._current_path = None
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
                self._refresh_table(data)

    def _delete_shortcut(self):
        row = self.table.currentRow()
        if row < 0 or not self._current_path:
            return
        data = _load_preset(self._current_path)
        data.pop(row)
        _save_preset(self._current_path, data)
        self._refresh_table(data)

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

from PyQt6.QtWidgets import QFileDialog

class AppMappingPanel(QWidget):
    """Shows which .exe names map to the current preset, with add/remove."""

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
        # File picker for .exe
        exe_path, _ = QFileDialog.getOpenFileName(
            self, "Select Application", "C:/", "Executables (*.exe)"
        )
        if not exe_path:
            return
        exe_name = os.path.basename(exe_path)   # e.g. "Code.exe"

        app_label, ok1 = QInputDialog.getText(self, "App Name", "Display name:")
        category_str, ok2 = QInputDialog.getText(self, "Category", "Category (e.g. development):")
        if not (ok1 and ok2):
            return

        # Build relative shortcut_file path to match existing convention
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
