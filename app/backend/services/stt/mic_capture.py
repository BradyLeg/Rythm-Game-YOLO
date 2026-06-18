"""Microphone capture using sounddevice. Records audio and saves to a temp .wav file."""

import os
import tempfile
import wave
import numpy as np
import sounddevice as sd

SAMPLE_RATE = 16000  # 16kHz mono — what Whisper expects
CHANNELS = 1
SOUND_TEMP_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "sound-temp")


def record_audio(duration_sec: float = 4.0, sample_rate: int = SAMPLE_RATE) -> str:
    """Record from default mic and return path to a .wav file in sound-temp/."""
    os.makedirs(SOUND_TEMP_DIR, exist_ok=True)

    audio = sd.rec(
        int(duration_sec * sample_rate),
        samplerate=sample_rate,
        channels=CHANNELS,
        dtype="int16",
    )
    sd.wait()

    fd, path = tempfile.mkstemp(suffix=".wav", dir=SOUND_TEMP_DIR)
    os.close(fd)
    with wave.open(path, "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(audio.tobytes())

    return path
