# Rhythm Game YOLO

A local Windows desktop application that combines voice control, AI-powered command routing, and computer vision to automate and interact with rhythm games. Packaged as a standalone `.exe`.

## Architecture

```
app/
├── frontend/          PyQt6 desktop GUI
│   ├── gui/           Main window, theming
│   └── components/    STT test, TTS toggle, YOLO section, controller test
├── backend/
│   ├── api/           FastAPI REST endpoints
│   ├── orchestrator/  Master pipeline (mic → whisper → LLM → keypress → TTS)
│   └── services/
│       ├── stt/       Mic capture, combat command parser
│       ├── llm/       Command router (Ollama tool-calling)
│       ├── tts/       (handled via integrations)
│       ├── input/     Keyboard handler (pydirectinput)
│       └── vision/    YOLO gameplay automation (WIP)
├── integrations/
│   ├── whisper/       Speech-to-text (Whisper Small, local)
│   ├── miku_tts/     Text-to-speech (Hugging Face Miku RVC Space)
│   ├── gpt_oss_20b/  Local LLM via Ollama
│   └── yolo/         Vision detection (WIP)
├── models/            Local model weights
│   ├── stt/           small.pt (Whisper)
│   └── vision/        YOLO weights (not yet trained)
└── packaging/         PyInstaller / .exe build config
```

## Features

| Feature | Status |
|---------|--------|
| Voice command recognition (Whisper Small) | ✅ Working |
| LLM command routing (gpt-oss:20b via Ollama) | ✅ Working |
| Keyboard automation (pydirectinput) | ✅ Working |
| Miku TTS voice responses (HF Space + pyttsx3 fallback) | ✅ Working |
| Combat command parser (enemy + direction → combos) | ✅ Working |
| PyQt6 GUI with test panels | ✅ Working |
| FastAPI backend | ✅ Working |
| YOLO gameplay vision automation | ✅ Working |
| .exe packaging | 🚧 Not started |

## Prerequisites

- **Python 3.13+** (tested on 3.13)
- **Windows 10/11** (required for pydirectinput)
- **FFmpeg** installed and on PATH (required by Whisper)
- **Ollama** running locally with the `gpt-oss:20b` model pulled
- **Microphone** for voice input

## Setup

```powershell
# Clone the repo
git clone <repo-url>
cd Rythm-Game-YOLO

# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### Ollama (LLM)

```powershell
# Install Ollama from https://ollama.com, then:
ollama pull gpt-oss:20b
```

Ollama must be running on `http://localhost:11434` (default). Override with the `LLM_BASE_URL` environment variable if needed.

### FFmpeg

Download from https://ffmpeg.org/download.html and add to your system PATH.

## Running

### GUI (primary interface)

```powershell
python -m app.frontend.main
```

The **YOLO Gameplay Automation** button in the GUI starts real-time screen capture and detection. It uses the trained model at `app/models/vision/best.pt` to detect gameplay elements and automatically sends the corresponding keypresses.

### FastAPI backend (for API/testing)

```powershell
uvicorn app.backend.api.routes:app --reload
```

API is available at `http://127.0.0.1:8000`. Key endpoints:
- `GET /api/health` — health check
- `POST /api/process` — send `{"text": "..."}` or `{"text": "TRIGGER_LIVE_MIC"}` for mic recording

### Smoke tests

```powershell
python test_llm.py              # Tests LLM routing (requires Ollama)
python test_tts.py              # Tests Miku TTS (requires internet)
python test_complete_backend.py # Full pipeline with live mic
```

## Project Structure

| Directory | Purpose |
|-----------|---------|
| `app/frontend/` | PyQt6 GUI — launch point is `main.py` |
| `app/backend/api/` | FastAPI routes |
| `app/backend/orchestrator/` | Ties STT → LLM → keyboard → TTS together |
| `app/backend/services/` | Individual service layers |
| `app/integrations/` | External model/API adapters |
| `app/models/` | Local model weight files (git-ignored `.pt` files) |
| `app/tests/` | Automated tests |
| `app/packaging/` | `.exe` build scripts |
| `sound-temp/` | Ephemeral mic recordings (git-ignored) |

## How It Works

1. **Voice input** — Mic records audio (4s window) via `sounddevice`
2. **Transcription** — Whisper Small converts speech to text locally
3. **Routing** — Either the combat command parser handles it directly, or the LLM (gpt-oss:20b) interprets intent via tool-calling
4. **Execution** — `pydirectinput` sends the mapped keypress to the active window
5. **Feedback** — Miku TTS speaks a response back to the player

## Contributing

Each team member has a `*_TASKLIST.md` file tracking their assigned work. The shared `TASKLIST.md` covers the overall project roadmap.
