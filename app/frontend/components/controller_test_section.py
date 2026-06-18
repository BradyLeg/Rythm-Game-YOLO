import os
import wave
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton
from PyQt6.QtCore import QThread, pyqtSignal, Qt


KEY_ACTION_MAP = {
    Qt.Key.Key_Up: "move_up",
    Qt.Key.Key_Down: "move_down",
    Qt.Key.Key_Left: "move_left",
    Qt.Key.Key_Right: "move_right",
    Qt.Key.Key_Return: "select",
    Qt.Key.Key_Escape: "go_back",
    Qt.Key.Key_Space: "start_game",
}

MIKU_LINES = {
    "move_up": "Scrolling up now!",
    "move_down": "Going down here!",
    "move_left": "Moving to left!",
    "move_right": "Moving to right!",
    "select": "Selected, let's go!",
    "go_back": "Going back now!",
    "start_game": "Starting the game!",
}


class TTSPlayWorker(QThread):
    """Generate Miku TTS, play in memory, delete file after."""
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, text: str):
        super().__init__()
        self.text = text

    def run(self):
        path = ""
        try:
            import sounddevice as sd
            import numpy as np
            from app.integrations.miku_tts.tts import MikuTTSClient

            client = MikuTTSClient()
            path = client.speak(self.text)

            if not path or not os.path.exists(path):
                self.error.emit("No audio file generated")
                return

            # Load into memory and play
            with wave.open(path, "rb") as wf:
                frames = wf.readframes(wf.getnframes())
                audio = np.frombuffer(frames, dtype=np.int16)
                sd.play(audio, samplerate=wf.getframerate())
                sd.wait()

            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))
        finally:
            if path and os.path.exists(path):
                try:
                    os.remove(path)
                except OSError:
                    pass


class ControllerTestSection(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._tts_worker = None
        self._build_ui()
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        label = QLabel("Controller Test (Press game keys here)")
        label.setObjectName("section-label")
        layout.addWidget(label)

        self.focus_btn = QPushButton("🎮 Click to activate key capture")
        self.focus_btn.setObjectName("accent-btn")
        self.focus_btn.clicked.connect(self._grab_focus)
        layout.addWidget(self.focus_btn)

        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setPlaceholderText("Press ↑ ↓ ← → Enter Esc Space while focused...")
        self.log.setMaximumHeight(140)
        layout.addWidget(self.log)

    def _grab_focus(self):
        self.setFocus()
        self.log.append("✅ Key capture active. Press a game key!")

    def keyPressEvent(self, event):
        action = KEY_ACTION_MAP.get(event.key())
        if action is None:
            return super().keyPressEvent(event)

        line = MIKU_LINES[action]
        self.log.append(f"⌨️ {action} → 🔊 \"{line}\"")
        self._speak(line)

    def _speak(self, text: str):
        if self._tts_worker and self._tts_worker.isRunning():
            return
        self._tts_worker = TTSPlayWorker(text)
        self._tts_worker.finished.connect(self._on_done)
        self._tts_worker.error.connect(self._on_error)
        self._tts_worker.start()

    def _on_done(self):
        self.log.append("✅ Playback complete.")

    def _on_error(self, msg: str):
        self.log.append(f"❌ TTS error: {msg}")
