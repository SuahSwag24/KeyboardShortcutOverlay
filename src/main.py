import sys
from PyQt6.QtWidgets import QApplication
from components.keyboard_listener import KeySignalEmitter
from components.overlay import Overlay
from components.system_tray_menu import setup_system_tray

app = QApplication(sys.argv)
app.setQuitOnLastWindowClosed(False)

overlay = Overlay()
emitter = KeySignalEmitter()

tray_icon = setup_system_tray(app)

emitter.keys_changed.connect(overlay.update_keys)
emitter.quit_app.connect(app.quit)
emitter.shortcut_executed.connect(overlay.flash_shortcut)

overlay.show()
emitter.start()
app.exec()