from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import pyqtSignal


class TTSSection(QWidget):
    toggled = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        label = QLabel("TTS Commentary")
        label.setObjectName("section-label")
        layout.addWidget(label)

        self.tts_toggle = QPushButton("TTS: OFF")
        self.tts_toggle.setCheckable(True)
        self.tts_toggle.setObjectName("toggle-btn")
        self.tts_toggle.toggled.connect(self._on_toggled)
        layout.addWidget(self.tts_toggle)

        layout.addStretch()

    def _on_toggled(self, checked: bool):
        self.tts_toggle.setText("TTS: ON" if checked else "TTS: OFF")
        self.toggled.emit(checked)

    def set_enabled(self, enabled: bool):
        self.tts_toggle.setChecked(enabled)
