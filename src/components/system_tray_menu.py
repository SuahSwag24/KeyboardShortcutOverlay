from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtWidgets import QSystemTrayIcon, QMenu, QStyle

def setup_system_tray(app, config_menu):
    icon = QIcon(app.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon))

    tray = QSystemTrayIcon(app)
    tray.setIcon(icon)
    tray.setToolTip("Keyboard Shortcut Overlay")
    tray.setVisible(True)

    menu = QMenu()

    quit_action = QAction("Exit Program", menu)
    quit_action.triggered.connect(app.quit)

    open_config_action = QAction("Configure", menu)
    open_config_action.triggered.connect(config_menu.show_window)

    menu.addAction(quit_action)
    menu.addAction(open_config_action)

    tray.setContextMenu(menu)
    tray.show()

    return tray