import os
import logging
import numpy as np
from ultralytics import YOLO

logger = logging.getLogger("YOLOAdapter")

WEIGHTS_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "models", "vision", "best.pt")


class YOLODetector:
    """Loads a YOLO model and runs inference on frames."""

    def __init__(self, weights: str = WEIGHTS_PATH, conf: float = 0.5):
        self.model = YOLO(weights)
        self.conf = conf
        logger.info(f"YOLO model loaded from {weights}")

    def detect(self, frame: np.ndarray) -> list[dict]:
        """Run detection on a BGR numpy frame. Returns list of {label, conf, box}."""
        results = self.model.predict(frame, conf=self.conf, verbose=False)
        detections = []
        for r in results:
            for box in r.boxes:
                detections.append({
                    "label": r.names[int(box.cls[0])],
                    "conf": float(box.conf[0]),
                    "box": box.xyxy[0].tolist(),
                })
        return detections
