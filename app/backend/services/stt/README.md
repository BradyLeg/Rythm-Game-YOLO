# stt

Speech-to-text support and the transcription-to-action mapping live here.

Purpose
- Host the local transcription wrappers (Whisper-small) and the converter that maps recognized text to input actions.

Responsibilities
- Provide a stable interface that returns normalized commands (e.g. `"press_up"`, `"tap_x"`, `"start_hold"`).
- Validate and sanitize transcripts before passing to the `input` service.
- Provide configuration for phrase-to-action mapping and confidence thresholds.

Notes for implementation
- Keep transcription code separate from mapping logic; export small, testable functions.
- Consider using VAD (voice activity detection) and short buffers to reduce latency.
- Add unit tests for common phrases and edge cases.

Suggested libraries/tools
- Model: Whisper-small (local)
- Python helpers: `whisper` wrappers or `faster-whisper` for performance
- Optional: `webrtcvad` for voice activity detection

Integration
- This service should call the `input` service to perform the actual keyboard/gamepad actions.
