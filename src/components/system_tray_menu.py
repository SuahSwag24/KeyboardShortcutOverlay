from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtWidgets import QSystemTrayIcon, QMenu, QStyle

def setup_system_tray(app, config_menu, keyboard_listener):
    icon = QIcon(app.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon))

    tray = QSystemTrayIcon(app)
    tray.setIcon(icon)
    tray.setToolTip("Keyboard Shortcut Overlay")
    tray.setVisible(True)

    menu = QMenu()

    reset_keys_action = QAction("Reset Keys", menu)
    reset_keys_action.triggered.connect(keyboard_listener.reset_keys_pressed)
    
    open_config_action = QAction("Configure", menu)
    open_config_action.triggered.connect(config_menu.show_window)

    quit_action = QAction("Exit Program", menu)
    quit_action.triggered.connect(app.quit)

    menu.addAction(reset_keys_action)
    menu.addAction(open_config_action)
    menu.addAction(quit_action)

    tray.setContextMenu(menu)
    tray.show()

    return tray