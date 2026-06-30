import sys
from PyQt6.QtWidgets import QApplication
from components.window_changed import WindowChangeNotification
from utils.timer_util import BackgroundTimerUtil
from components.keyboard_listener import KeySignalEmitter
from components.overlay import Overlay
from components.system_tray_menu import setup_system_tray
from components.configuration_menu import ConfigurationWindow

app = QApplication(sys.argv)
app.setQuitOnLastWindowClosed(False)

overlay = Overlay()
emitter = KeySignalEmitter()
config_menu = ConfigurationWindow(emitter, on_shortcuts_changed=overlay.reload_shortcuts)

tray_icon = setup_system_tray(app, config_menu, emitter)

timer_manager = BackgroundTimerUtil(1000)
timer_manager.start_all()

notif = WindowChangeNotification()
timer_manager.window_changed.connect(notif.notify)

emitter.keys_changed.connect(overlay.update_keys)
emitter.quit_app.connect(app.quit)
emitter.shortcut_executed.connect(overlay.animate_execute)

config_menu.general_tab.opacity_changed.connect(overlay.set_opacity)
config_menu.general_tab.text_opacity_changed.connect(overlay.set_text_opacity)
config_menu.general_tab.font_size_changed.connect(overlay.set_font_size)
config_menu.general_tab.list_item_count_changed.connect(overlay.set_list_item_count)
config_menu.general_tab.overlay_width_changed.connect(overlay.set_overlay_width)
config_menu.general_tab.overlay_x_offset_changed.connect(overlay.set_overlay_x_offset)
config_menu.general_tab.overlay_y_offset_changed.connect(overlay.set_overlay_y_offset)

overlay.show()
emitter.start()
app.exec()