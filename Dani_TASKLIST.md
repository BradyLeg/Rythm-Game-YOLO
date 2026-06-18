# Dani — GUI Frontend + STT Integration

## Working Folders

- `app/frontend/gui/` — Main desktop GUI window and layout
- `app/frontend/components/` — Reusable UI components (buttons, status indicators)
- `app/integrations/whisper/` — Whisper Small STT adapter
- `app/backend/api/` — API endpoints the frontend calls
- `app/tests/` — Tests for frontend and STT

---

## Required Software

| Tool | Purpose | Install |
|------|---------|---------|
| Python 3.10+ | Runtime | https://www.python.org/downloads/ |
| pip | Package manager | Included with Python |
| PyQt5 or Tkinter | Desktop GUI framework | `pip install pyqt5` (or use built-in tkinter) |
| OpenAI Whisper | Speech-to-text model | `pip install openai-whisper` |
| FFmpeg | Audio processing (required by Whisper) | https://ffmpeg.org/download.html — add to PATH |
| PyAudio or sounddevice | Microphone capture | `pip install sounddevice` |
| requests or httpx | HTTP client for backend calls | `pip install httpx` |
| pytest | Testing | `pip install pytest` |

---

## Environment Setup

All dependencies run inside a Python virtual environment. Do **not** install globally.

```powershell
# From the project root (Rythm-Game-YOLO/)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install all project dependencies
pip install -r requirements.txt
```

You'll see `(venv)` in your prompt when active. To deactivate: `deactivate`

> **Note:** FFmpeg must still be installed system-wide and added to PATH (not a pip package).

---

## Tasks

### 1. Set Up GUI Shell ✅

- [x] Choose GUI framework (PyQt6 for desktop `.exe`)
- [x] Create main window with title bar and basic layout
- [x] Add a status label showing current system state (Idle, Listening, Processing)
- [x] Add a "Start Listening" / "Stop Listening" toggle button
- [x] Add a text area showing transcription output and LLM responses

### 2. Implement Microphone Capture ✅

- [x] Use `sounddevice` to record audio from default microphone
- [x] Record in chunks (4 seconds of 16kHz mono int16 audio)
- [x] Save audio buffer to a temporary `.wav` file for Whisper processing
- [x] Wire mic capture to GUI button with QThread (non-blocking)

### 3. Integrate Whisper Small (STT) ✅

- [x] Load Whisper Small model locally in `app/integrations/whisper/`
- [x] Create a function `transcribe(audio_path: str) -> str` that returns text
- [x] Wire microphone capture → transcription → display in GUI text area
- [x] Handle edge cases: empty audio, background noise, short utterances

### 4. Connect Frontend to Backend API ✅

- [x] Send transcribed text to `POST /api/process` on the FastAPI backend
- [x] Display LLM response in GUI text area
- [x] Show loading/processing indicator while waiting for backend response

### 5. GUI Polish & UX

- [ ] Add visual feedback when mic is active (color change or icon)
- [ ] Add error dialogs for missing mic or model load failures
- [ ] Ensure GUI remains responsive during transcription (use threading)

---

## Suggested Tests

Write tests in `app/tests/test_stt.py` and `app/tests/test_frontend.py`:

```python
# test_stt.py
def test_transcribe_returns_string():
    """Whisper transcribe() returns a non-empty string for valid audio."""
    from app.integrations.whisper.stt import transcribe
    result = transcribe("app/tests/fixtures/sample_hello.wav")
    assert isinstance(result, str)
    assert len(result) > 0

def test_transcribe_empty_audio():
    """Whisper handles silent/empty audio gracefully."""
    from app.integrations.whisper.stt import transcribe
    result = transcribe("app/tests/fixtures/silence.wav")
    assert isinstance(result, str)  # may be empty string, should not crash

def test_transcribe_known_phrase():
    """Whisper correctly detects a known command phrase."""
    from app.integrations.whisper.stt import transcribe
    result = transcribe("app/tests/fixtures/say_move_up.wav")
    assert "move up" in result.lower() or "up" in result.lower()
```

```python
# test_frontend.py
def test_gui_window_opens():
    """Main window initializes without errors."""
    from app.frontend.gui.main_window import MainWindow
    window = MainWindow()
    assert window is not None

def test_status_label_default():
    """Status label starts as 'Idle'."""
    from app.frontend.gui.main_window import MainWindow
    window = MainWindow()
    assert window.status_label.text() == "Idle"
```

---

## Notes

- Use threading or `asyncio` to keep GUI responsive during model inference.
- Whisper Small model will be downloaded on first run (~460 MB). Store in `app/models/stt/`.
- Coordinate with Brady on the backend API contract (`POST /api/process` request/response format).
