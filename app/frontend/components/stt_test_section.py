from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTextEdit, QComboBox,
    QLineEdit, QCheckBox,
)
from PyQt6.QtCore import pyqtSignal, QThread, Qt
import os


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


class TranscribeWorker(QThread):
    """Runs Whisper transcription on a background thread."""
    finished = pyqtSignal(str)  # emits transcribed text
    error = pyqtSignal(str)

    def __init__(self, wav_path: str):
        super().__init__()
        self.wav_path = wav_path

    def run(self):
        try:
            from app.integrations.whisper.stt import transcribe
            text = transcribe(self.wav_path)
            self.finished.emit(text)
        except Exception as e:
            self.error.emit(str(e))


class APIWorker(QThread):
    finished = pyqtSignal(str, str)  # response text, action
    error = pyqtSignal(str)

    def __init__(self, text: str, url: str = "http://127.0.0.1:8000/api/process"):
        super().__init__()
        self.text = text
        self.url = url

    def run(self):
        try:
            import httpx
            r = httpx.post(self.url, json={"text": self.text}, timeout=30.0)
            r.raise_for_status()
            data = r.json()
            self.finished.emit(data.get("response", ""), data.get("action", ""))
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

        # Header row with label + toggle in top-right
        header_row = QHBoxLayout()
        label = QLabel("Speech Recognition Test")
        label.setObjectName("section-label")
        header_row.addWidget(label)
        header_row.addStretch()
        self.text_input_toggle = QCheckBox("Text Input")
        self.text_input_toggle.toggled.connect(self._on_toggle_text_input)
        header_row.addWidget(self.text_input_toggle)
        layout.addLayout(header_row)

        phrase_row = QHBoxLayout()
        self.phrase_combo = QComboBox()
        self.phrase_combo.addItems(PHRASES)
        phrase_row.addWidget(self.phrase_combo)

        self.stt_btn = QPushButton("\U0001f3a4 Test STT")
        self.stt_btn.setObjectName("accent-btn")
        self.stt_btn.clicked.connect(self._on_test_clicked)
        phrase_row.addWidget(self.stt_btn)
        layout.addLayout(phrase_row)

        # Text input (hidden by default)
        self.text_input = QLineEdit()
        self.text_input.setPlaceholderText("Type a command (e.g. 'Bat left')...")
        self.text_input.returnPressed.connect(self._on_text_submit)
        self.text_input.setVisible(False)
        layout.addWidget(self.text_input)

        self.stt_output = QTextEdit()
        self.stt_output.setReadOnly(True)
        self.stt_output.setPlaceholderText("STT results will appear here...")
        self.stt_output.setMaximumHeight(120)
        layout.addWidget(self.stt_output)

    def _on_toggle_text_input(self, checked: bool):
        self.text_input.setVisible(checked)

    def _on_text_submit(self):
        text = self.text_input.text().strip()
        if text:
            self._on_transcribe_done(text)
            self.text_input.clear()

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
        self.stt_output.setText("⏳ Transcribing...")
        self._transcribe_worker = TranscribeWorker(wav_path)
        self._transcribe_worker.finished.connect(self._on_transcribe_done)
        self._transcribe_worker.error.connect(self._on_transcribe_error)
        self._transcribe_worker.finished.connect(lambda _: self._cleanup_wav(wav_path))
        self._transcribe_worker.error.connect(lambda _: self._cleanup_wav(wav_path))
        self._transcribe_worker.start()

    def _cleanup_wav(self, path: str):
        try:
            if path and os.path.exists(path):
                os.remove(path)
        except OSError:
            pass

    def _on_transcribe_done(self, text: str):
        if not text:
            self.stt_btn.setEnabled(True)
            self.stt_output.setText("⚠️ No speech detected.")
            return

        # Check for combat command first
        from app.backend.services.stt.combat_commands import parse_command, execute_combat
        result = parse_command(text)
        if result:
            enemy, combo, direction = result
            execute_combat(enemy, direction)
            dir_label = direction or "none"
            self.stt_btn.setEnabled(True)
            self.stt_output.setText(
                f"🗣️ \"{text}\"\n⚔️ {enemy} | Dir: {dir_label} | Combo: {combo}"
            )
            return

        self.stt_output.setText(f"🗣️ \"{text}\"\n⏳ Sending to backend...")
        self._api_worker = APIWorker(text)
        self._api_worker.finished.connect(self._on_api_done)
        self._api_worker.error.connect(self._on_api_error)
        self._api_worker.start()

    def _on_api_done(self, response: str, action: str):
        self.stt_btn.setEnabled(True)
        self.stt_output.setText(f"🤖 {response}\n⚡ Action: {action}")
        self.test_requested.emit(self.phrase_combo.currentText())

    def _on_api_error(self, msg: str):
        self.stt_btn.setEnabled(True)
        self.stt_output.append(f"\n❌ Backend error: {msg}")

    def _on_transcribe_error(self, msg: str):
        self.stt_btn.setEnabled(True)
        self.stt_output.setText(f"❌ Transcription error: {msg}")

    def _on_record_error(self, msg: str):
        self.stt_btn.setEnabled(True)
        self.stt_output.setText(f"❌ Mic error: {msg}")

    def set_result(self, text: str):
        self.stt_output.setText(text)

    def current_phrase(self) -> str:
        return self.phrase_combo.currentText()
