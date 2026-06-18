from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt


class TitleBar(QWidget):
    def __init__(self, text: str = "Rhythm Game YOLO", parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.label = QLabel(text)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName("title")
        layout.addWidget(self.label)

    def set_text(self, text: str):
        self.label.setText(text)
