# Rythm-Game-YOLO

This project is a local Windows desktop application intended to be packaged as a `.exe`, not a webpage.

It is organized around reusable components and service boundaries for:

- Speech to text with Whisper-small
- Local language-model routing with gpt-oss-20b
- Text to speech with MIKU TTS
- Rhythm-game vision automation with YOLO

Primary structure:

- `app/frontend` for the desktop GUI
- `app/backend` for FastAPI and orchestration
- `app/models` for local model assets and notes
- `app/integrations` for API and model adapters
- `app/packaging` for `.exe` build and release work
- `app/tests` for automated tests

Each directory contains its own README placeholder with guidance for that area.