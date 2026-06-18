"""Whisper Small speech-to-text adapter."""

import os
import wave
import whisper

_MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "models", "stt")
_model = None


def _load_model():
    """Lazy-load Whisper Small model, caching for reuse."""
    global _model
    if _model is None:
        os.makedirs(_MODEL_DIR, exist_ok=True)
        _model = whisper.load_model("small", download_root=_MODEL_DIR)
    return _model


def transcribe(audio_path: str) -> str:
    """Transcribe a .wav file and return the text.

    Returns empty string for silent/empty audio or on errors.
    """
    if not os.path.isfile(audio_path):
        return ""

    # Reject files that are too short (< 0.5s of audio)
    try:
        with wave.open(audio_path, "rb") as wf:
            frames = wf.getnframes()
            rate = wf.getframerate()
            if frames / rate < 0.5:
                return ""
    except Exception:
        return ""

    try:
        model = _load_model()
        result = model.transcribe(audio_path, fp16=False)
        return result.get("text", "").strip()
    except Exception:
        return ""
