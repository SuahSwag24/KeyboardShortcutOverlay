import sys
from PyQt6.QtWidgets import QApplication
from components.window_changed import WindowChangeNotification
from utils.timer_util import BackgroundTimerUtil
from components.window_focus_listener import get_focused_window
from components.keyboard_listener import KeySignalEmitter
from components.overlay import Overlay
from components.system_tray_menu import setup_system_tray
from components.configuration_menu import ConfigurationWindow

app = QApplication(sys.argv)
app.setQuitOnLastWindowClosed(False)

overlay = Overlay()
emitter = KeySignalEmitter()
config_menu = ConfigurationWindow()

tray_icon = setup_system_tray(app, config_menu)

timer_manager = BackgroundTimerUtil(1000)
timer_manager.start_all()

notif = WindowChangeNotification()
timer_manager.window_changed.connect(notif.notify)

emitter.keys_changed.connect(overlay.update_keys)
emitter.quit_app.connect(app.quit)
emitter.shortcut_executed.connect(overlay.animate_execute)

overlay.show()
emitter.start()
app.exec()