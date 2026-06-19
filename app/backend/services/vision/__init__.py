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
    "Arrow_Right": "move_right",
    "Arrow_Up": "move_up",
    "Hold_Start": "move_up",
    "Hold_End": "move_up",
}

ARROW_LABELS = {"Arrow_Right", "Arrow_Up", "Hold_Start", "Hold_End"}
ENEMY_LABELS = {"Enemy", "Enemy_Special"}


def _boxes_overlap(box_a: list, box_b: list) -> bool:
    """Check if two [x1, y1, x2, y2] boxes overlap."""
    return (box_a[0] < box_b[2] and box_a[2] > box_b[0] and
            box_a[1] < box_b[3] and box_a[3] > box_b[1])


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
        """Press arrow keys when an Enemy overlaps with them."""
        if not detections:
            return
        enemies = [d for d in detections if d["label"] in ENEMY_LABELS]
        arrows = [d for d in detections if d["label"] in ARROW_LABELS]

        for arrow in arrows:
            for enemy in enemies:
                if _boxes_overlap(arrow["box"], enemy["box"]):
                    action = LABEL_TO_ACTION.get(arrow["label"])
                    if action:
                        logger.info(f"🎯 [{enemy['label']}] overlaps [{arrow['label']}] → pressing {action}")
                        self._keyboard.press_action_key(action)
                    break
