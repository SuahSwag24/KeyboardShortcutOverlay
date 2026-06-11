from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt

class ConfigurationWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Test")
        self.resize(400, 300)

        layout = QVBoxLayout()

        self.label = QLabel("Configuration Screen", self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)

        self.setLayout(layout)

    def show_window(self):
        self.show()
        self.raise_()
        self.activateWindow()