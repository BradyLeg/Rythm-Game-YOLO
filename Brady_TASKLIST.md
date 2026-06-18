# Brady — LLM + TTS Integration

## Working Folders

- `app/integrations/gpt-oss-20b/` — LLM adapter and prompt templates
- `app/integrations/miku-tts/` — MIKU TTS client adapter
- `app/backend/orchestrator/` — Pipeline logic (STT text → LLM → TTS → action)
- `app/backend/api/` — FastAPI routes
- `app/backend/services/` — Business logic / tool-calling layer
- `app/models/llm/` — Model config and notes
- `app/tests/` — Tests for LLM, TTS, and orchestrator

---

## Required Software

| Tool | Purpose | Install |
|------|---------|---------|
| Python 3.10+ | Runtime | https://www.python.org/downloads/ |
| pip | Package manager | Included with Python |
| FastAPI | Backend web framework | `pip install fastapi` |
| Uvicorn | ASGI server for FastAPI | `pip install uvicorn[standard]` |
| httpx | HTTP client (for TTS API calls) | `pip install httpx` |
| transformers | Load gpt-oss-20b model | `pip install transformers` |
| torch | PyTorch (model inference) | `pip install torch` (see https://pytorch.org for GPU build) |
| accelerate | Efficient model loading | `pip install accelerate` |
| pytest | Testing | `pip install pytest` |
| pytest-asyncio | Async test support | `pip install pytest-asyncio` |

---

## Environment Setup

All dependencies run inside a Python virtual environment. Do **not** install globally.

```powershell
# From the project root (Rythm-Game-YOLO/)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install all project dependencies
pip install -r requirements.txt

# Install additional packages for your tasks
pip install fastapi uvicorn[standard] transformers accelerate pytest-asyncio
```

You'll see `(venv)` in your prompt when active. To deactivate: `deactivate`

After installing new packages, update the shared requirements file:

```powershell
pip freeze > requirements.txt
```

---

## Tasks

### 1. Set Up FastAPI Backend

- [ ] Create `app/backend/api/routes.py` with a `POST /api/process` endpoint
- [ ] Accept JSON body: `{ "text": "user transcription here" }`
- [ ] Return JSON: `{ "response": "...", "action": "...", "tts_audio_url": "..." }`
- [ ] Add health check route `GET /api/health`
- [ ] Run locally with `uvicorn app.backend.api.routes:app --reload`

### 2. Integrate gpt-oss-20b (LLM)

- [ ] Load gpt-oss-20b model in `app/integrations/gpt-oss-20b/llm.py`
- [ ] Create function `generate_response(prompt: str) -> dict` returning text + action
- [ ] Design system prompt that interprets rhythm-game voice commands
- [ ] Implement tool-calling schema (e.g., `move_up`, `select`, `go_back`, `start_game`)
- [ ] Add timeout and error handling for inference

### 3. Implement Tool-Calling / Action Router

- [ ] Define available tools/actions in `app/backend/services/actions.py`
- [ ] Map LLM output to concrete game actions (keyboard presses, navigation)
- [ ] Log each action for debugging

### 4. Integrate MIKU TTS

- [ ] Create TTS client in `app/integrations/miku-tts/tts.py`
- [ ] Function `speak(text: str) -> str` that sends text to MIKU TTS and returns audio path/URL
- [ ] Play audio response back to user or provide path to frontend
- [ ] Handle TTS service unavailability gracefully

### 5. Build Orchestrator Pipeline

- [ ] In `app/backend/orchestrator/pipeline.py`, wire: text input → LLM → action + TTS
- [ ] Ensure pipeline returns both the action taken and spoken feedback
- [ ] Add logging at each pipeline stage for debugging

---

## Suggested Tests

Write tests in `app/tests/test_llm.py`, `app/tests/test_tts.py`, and `app/tests/test_orchestrator.py`:

```python
# test_llm.py
def test_llm_returns_response():
    """LLM generates a non-empty response for a valid prompt."""
    from app.integrations.gpt_oss_20b.llm import generate_response
    result = generate_response("move up in the menu")
    assert "response" in result
    assert len(result["response"]) > 0

def test_llm_returns_action():
    """LLM identifies an action from a navigation command."""
    from app.integrations.gpt_oss_20b.llm import generate_response
    result = generate_response("go to settings")
    assert "action" in result
    assert result["action"] in ["navigate", "select", "move_up", "move_down", "go_back"]

def test_llm_handles_gibberish():
    """LLM does not crash on nonsense input."""
    from app.integrations.gpt_oss_20b.llm import generate_response
    result = generate_response("asdfghjkl")
    assert "response" in result
```

```python
# test_tts.py
def test_tts_returns_audio_path():
    """TTS returns a valid audio file path."""
    from app.integrations.miku_tts.tts import speak
    path = speak("Moving up.")
    assert path.endswith(".wav") or path.endswith(".mp3")

def test_tts_handles_empty_string():
    """TTS handles empty input without crashing."""
    from app.integrations.miku_tts.tts import speak
    path = speak("")
    assert path is None or isinstance(path, str)
```

```python
# test_orchestrator.py
def test_pipeline_end_to_end():
    """Full pipeline processes text and returns action + spoken response."""
    from app.backend.orchestrator.pipeline import process
    result = process("select the first song")
    assert "action" in result
    assert "tts_audio" in result

def test_api_health_endpoint():
    """Health endpoint returns 200."""
    from fastapi.testclient import TestClient
    from app.backend.api.routes import app
    client = TestClient(app)
    response = client.get("/api/health")
    assert response.status_code == 200
```

---

## Notes

- gpt-oss-20b requires significant VRAM. Test with CPU first; switch to GPU for real-time use.
- Coordinate with Dani on the `POST /api/process` request/response contract.
- MIKU TTS is already hosted — confirm endpoint URL and auth requirements with team.
- Store prompt templates in `app/integrations/gpt-oss-20b/prompts/` for easy iteration.
