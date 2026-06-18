from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTextEdit, QComboBox,
)
from PyQt6.QtCore import pyqtSignal, QThread


PHRASES = [
    "Bat", "Slime", "Skeleton", "Zombie", "Ghost",
    "Mimic", "Witch", "Imp", "Armored Skeleton",
    "Shielded Zombie", "Fast Bat", "Split Slime",
    "Exploder", "Chain Enemy", "Teleporting Ghost",
    "Rhythm Mage", "Projectile Caster", "Shield Bearer",
    "Dash Enemy", "Boss Entity",
]


class RecordWorker(QThread):
    """Records audio on a background thread."""
    finished = pyqtSignal(str)  # emits wav file path
    error = pyqtSignal(str)

    def __init__(self, duration: float = 4.0):
        super().__init__()
        self.duration = duration

    def run(self):
        try:
            from app.backend.services.stt.mic_capture import record_audio
            path = record_audio(self.duration)
            self.finished.emit(path)
        except Exception as e:
            self.error.emit(str(e))


class STTTestSection(QWidget):
    test_requested = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._worker = None
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
        if self._worker and self._worker.isRunning():
            return  # already recording
        self.stt_btn.setEnabled(False)
        self.stt_output.setText("🎙️ Recording (4s)...")
        self._worker = RecordWorker(duration=4.0)
        self._worker.finished.connect(self._on_record_done)
        self._worker.error.connect(self._on_record_error)
        self._worker.start()

    def _on_record_done(self, wav_path: str):
        self.stt_btn.setEnabled(True)
        self.stt_output.setText(f"✅ Recorded: {wav_path}\nReady for transcription.")
        self.test_requested.emit(self.phrase_combo.currentText())

    def _on_record_error(self, msg: str):
        self.stt_btn.setEnabled(True)
        self.stt_output.setText(f"❌ Mic error: {msg}")

    def set_result(self, text: str):
        self.stt_output.setText(text)

    def current_phrase(self) -> str:
        return self.phrase_combo.currentText()
