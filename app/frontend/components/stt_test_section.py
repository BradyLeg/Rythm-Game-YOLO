from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTextEdit, QComboBox,
)
from PyQt6.QtCore import pyqtSignal


PHRASES = [
    "Bat", "Slime", "Skeleton", "Zombie", "Ghost",
    "Mimic", "Witch", "Imp", "Armored Skeleton",
    "Shielded Zombie", "Fast Bat", "Split Slime",
    "Exploder", "Chain Enemy", "Teleporting Ghost",
    "Rhythm Mage", "Projectile Caster", "Shield Bearer",
    "Dash Enemy", "Boss Entity",
]


class STTTestSection(QWidget):
    test_requested = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        label = QLabel("Speech Recognition Test")
        label.setObjectName("section-label")
        layout.addWidget(label)

        phrase_row = QHBoxLayout()
        self.phrase_combo = QComboBox()
        self.phrase_combo.addItems(PHRASES)
        phrase_row.addWidget(self.phrase_combo)

        self.stt_btn = QPushButton("\U0001f3a4 Test STT")
        self.stt_btn.setObjectName("accent-btn")
        self.stt_btn.clicked.connect(self._on_test_clicked)
        phrase_row.addWidget(self.stt_btn)
        layout.addLayout(phrase_row)

        self.stt_output = QTextEdit()
        self.stt_output.setReadOnly(True)
        self.stt_output.setPlaceholderText("STT results will appear here...")
        self.stt_output.setMaximumHeight(120)
        layout.addWidget(self.stt_output)

    def _on_test_clicked(self):
        phrase = self.phrase_combo.currentText()
        self.test_requested.emit(phrase)

    def set_result(self, text: str):
        self.stt_output.setText(text)

    def current_phrase(self) -> str:
        return self.phrase_combo.currentText()
