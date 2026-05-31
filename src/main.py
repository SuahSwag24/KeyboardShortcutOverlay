import sys
from PyQt6.QtWidgets import QApplication
from components.keyboard_listener import KeySignalEmitter
from components.overlay import Overlay

app = QApplication(sys.argv)
overlay = Overlay()
emitter = KeySignalEmitter()
emitter.keys_changed.connect(overlay.update_keys)
emitter.quit_app.connect(app.quit)

overlay.show()
emitter.start()
app.exec()