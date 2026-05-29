# whisper

Whisper-small integration and integration notes.

Purpose
- Store adapters and helpers for running the Whisper-small model locally and producing clean transcript output.

What to include
- Model-loading wrappers and performance tuning notes (batching, chunk size).
- Transcription normalization and confidence extraction.
- Small examples showing how to call the STT service and return a normalized command.

Integration note
- Transcripts that represent actionable commands should be normalized and routed to the `app/backend/services/input` service.
