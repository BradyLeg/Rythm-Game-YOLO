# Gabby — YOLO Integration + Computer Vision Training

## Working Folders

- `app/integrations/yolo/` — YOLO model loading, inference, and key-press logic
- `app/models/vision/` — Trained model weights, dataset configs, and training scripts
- `app/tests/` — Tests for detection accuracy and input triggering

---

## Required Software

| Tool | Purpose | Install |
|------|---------|---------|
| Python 3.10+ | Runtime | https://www.python.org/downloads/ |
| pip | Package manager | Included with Python |
| ultralytics | YOLOv8 training and inference | `pip install ultralytics` |
| torch | PyTorch (GPU-accelerated inference) | `pip install torch torchvision` (see https://pytorch.org) |
| opencv-python | Image/frame capture and processing | `pip install opencv-python` |
| mss or dxcam | Fast screen capture on Windows | `pip install mss` or `pip install dxcam` |
| pydirectinput | Simulate key presses for the game | `pip install pydirectinput` |
| LabelImg or Roboflow | Annotate training data | `pip install labelImg` or use https://roboflow.com |
| pytest | Testing | `pip install pytest` |

---

## Environment Setup

All dependencies run inside a Python virtual environment. Do **not** install globally.

```powershell
# From the project root (Rythm-Game-YOLO/)
python -m venv venv
.\venv\Scripts\Activate.ps1
source venv/Scripts/activate

# Install all project dependencies
pip install -r requirements.txt

# Install additional packages for your tasks
pip install ultralytics opencv-python mss pydirectinput labelImg
```

You'll see `(venv)` in your prompt when active. To deactivate: `deactivate`

After installing new packages, update the shared requirements file:

```powershell
pip freeze > requirements.txt
```

---

## Tasks

### 1. Collect and Annotate Training Data

- [ ] Record gameplay footage from the target rhythm game (screen capture or video files)
- [ ] Extract frames at a consistent rate (e.g., every 50ms for fast note detection)
- [ ] Annotate note objects using bounding boxes (LabelImg or Roboflow)
- [ ] Define classes: `note_up`, `note_down`, `note_left`, `note_right` (adjust per game)
- [ ] Split dataset: 80% train / 10% val / 10% test
- [ ] Store dataset config in `app/models/vision/dataset.yaml`

### 2. Train YOLO Model

- [ ] Use YOLOv8n or YOLOv8s (nano/small — fast enough for real-time)
- [ ] Train with: `yolo detect train data=app/models/vision/dataset.yaml model=yolov8n.pt epochs=50`
- [ ] Evaluate mAP on test set — target ≥ 0.80 mAP@0.5
- [ ] Save best weights to `app/models/vision/best.pt`
- [ ] Document training metrics in `app/models/vision/training_notes.md`

### 3. Implement Real-Time Screen Capture

- [ ] In `app/integrations/yolo/capture.py`, capture game window frames using `mss` or `dxcam`
- [ ] Crop to the relevant gameplay area (exclude HUD/menus)
- [ ] Target ≥30 FPS capture rate for rhythm game timing

### 4. Implement YOLO Inference Pipeline

- [ ] In `app/integrations/yolo/detector.py`, load trained model from `best.pt`
- [ ] Create function `detect_notes(frame) -> list[Detection]` returning class, bbox, confidence
- [ ] Filter detections by confidence threshold (e.g., ≥ 0.6)
- [ ] Process detections in order of Y-position (closest to hit zone first)

### 5. Map Detections to Key Presses

- [ ] In `app/integrations/yolo/input.py`, map each note class to a keyboard key
- [ ] Use `pydirectinput` to send key presses to the game window
- [ ] Implement timing logic — press when note bbox crosses the hit zone Y-coordinate
- [ ] Add configurable delay offset for timing calibration

### 6. Main Game Loop

- [ ] In `app/integrations/yolo/game_loop.py`, combine: capture → detect → press
- [ ] Run loop continuously during gameplay
- [ ] Add start/stop control (can be triggered by voice command via Brady's orchestrator)
- [ ] Log detections and presses for performance tuning

---

## Suggested Tests

Write tests in `app/tests/test_yolo.py` and `app/tests/test_input.py`:

```python
# test_yolo.py
import cv2

def test_model_loads():
    """YOLO model loads without errors."""
    from app.integrations.yolo.detector import load_model
    model = load_model("app/models/vision/best.pt")
    assert model is not None

def test_detect_notes_on_sample_frame():
    """Detector returns detections on a known gameplay frame."""
    from app.integrations.yolo.detector import load_model, detect_notes
    model = load_model("app/models/vision/best.pt")
    frame = cv2.imread("app/tests/fixtures/gameplay_frame.png")
    detections = detect_notes(model, frame)
    assert isinstance(detections, list)
    assert len(detections) > 0

def test_detection_has_required_fields():
    """Each detection contains class, confidence, and bbox."""
    from app.integrations.yolo.detector import load_model, detect_notes
    model = load_model("app/models/vision/best.pt")
    frame = cv2.imread("app/tests/fixtures/gameplay_frame.png")
    detections = detect_notes(model, frame)
    for det in detections:
        assert "class" in det
        assert "confidence" in det
        assert "bbox" in det
        assert det["confidence"] >= 0.6

def test_no_detections_on_blank_frame():
    """Detector returns empty list on a blank image."""
    import numpy as np
    from app.integrations.yolo.detector import load_model, detect_notes
    model = load_model("app/models/vision/best.pt")
    blank = np.zeros((480, 640, 3), dtype=np.uint8)
    detections = detect_notes(model, blank)
    assert detections == []
```

```python
# test_input.py
def test_key_mapping_exists():
    """All note classes map to a valid key."""
    from app.integrations.yolo.input import KEY_MAP
    expected_classes = ["note_up", "note_down", "note_left", "note_right"]
    for cls in expected_classes:
        assert cls in KEY_MAP
        assert isinstance(KEY_MAP[cls], str)

def test_hit_zone_logic():
    """Note within hit zone triggers press, note above does not."""
    from app.integrations.yolo.input import should_press
    # bbox format: (x, y, w, h) — y is top of bbox
    assert should_press(bbox=(100, 450, 30, 30), hit_zone_y=460) is True
    assert should_press(bbox=(100, 200, 30, 30), hit_zone_y=460) is False
```

---

## Notes

- Start with `mss` for screen capture; switch to `dxcam` if FPS is too low.
- YOLOv8n is fastest; upgrade to YOLOv8s only if accuracy is insufficient.
- Timing calibration is critical — add a configurable ms offset in a config file.
- Coordinate with Brady to expose a `start_autoplay` / `stop_autoplay` action the LLM can trigger.
- Test with recorded video files before live gameplay to iterate faster.
