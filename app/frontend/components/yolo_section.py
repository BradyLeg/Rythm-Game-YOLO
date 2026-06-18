from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import pyqtSignal


class YOLOSection(QWidget):
    automate_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        label = QLabel("YOLO Gameplay Automation")
        label.setObjectName("section-label")
        layout.addWidget(label)

        self.yolo_btn = QPushButton("\u25b6 Automate Gameplay")
        self.yolo_btn.setObjectName("accent-btn")
        self.yolo_btn.clicked.connect(self._on_clicked)
        layout.addWidget(self.yolo_btn)

    def _on_clicked(self):
        self.automate_requested.emit()

    def set_running(self, running: bool):
        self.yolo_btn.setText(
            "\u25a0 Stop Automation" if running else "\u25b6 Automate Gameplay"
        )
