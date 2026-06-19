import logging
import threading
import time
import numpy as np
import mss
from app.integrations.yolo import YOLODetector
from app.backend.services.input.keyboard_handler import KeyboardHandler

logger = logging.getLogger("VisionService")

# Map YOLO class labels to keyboard action intents
LABEL_TO_ACTION = {
    "up": "move_up",
    "down": "move_down",
    "left": "move_left",
    "right": "move_right",
    "select": "select",
    "start": "start_game",
}


class VisionService:
    """Captures the screen in a loop, runs YOLO detection, and issues keypresses."""

    def __init__(self, fps: float = 10.0):
        self._detector = YOLODetector()
        self._keyboard = KeyboardHandler()
        self._running = False
        self._thread: threading.Thread | None = None
        self._interval = 1.0 / fps

    @property
    def running(self) -> bool:
        return self._running

    def start(self):
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()
        logger.info("Vision automation started")

    def stop(self):
        self._running = False
        if self._thread:
            self._thread.join(timeout=2.0)
            self._thread = None
        logger.info("Vision automation stopped")

    def _loop(self):
        with mss.mss() as sct:
            monitor = sct.monitors[1]  # primary monitor
            while self._running:
                frame = np.array(sct.grab(monitor))[:, :, :3]  # BGR
                detections = self._detector.detect(frame)
                self._act(detections)
                time.sleep(self._interval)

    def _act(self, detections: list[dict]):
        """Press keys based on highest-confidence detection."""
        if not detections:
            return
        best = max(detections, key=lambda d: d["conf"])
        action = LABEL_TO_ACTION.get(best["label"])
        if action:
            self._keyboard.press_action_key(action)
