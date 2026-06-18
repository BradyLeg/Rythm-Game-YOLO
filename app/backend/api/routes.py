import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.backend.orchestrator import GameOrchestrator

app = FastAPI(title="Hatsune Miku Rhythm Game Voice Gateway")

# Spin up master orchestrator on web app initialization
orchestrator = GameOrchestrator()

class ProcessRequest(BaseModel):
    text: str  

class ProcessResponse(BaseModel):
    response: str
    action: str
    tts_audio_url: str

@app.get("/api/health")
def health():
    return {"status": "ok"}

@app.post("/api/process", response_model=ProcessResponse)
def process(req: ProcessRequest):
    # Support both direct text simulation or physical microphone loops
    if req.text == "TRIGGER_LIVE_MIC":
        result = orchestrator.run_live_voice_pipeline(record_duration=4.0)
    else:
        result = orchestrator.handle_raw_text(req.text)

    local_audio_path = result.get("audio_path", "")
    web_audio_url = ""
    
    if local_audio_path:
        filename = os.path.basename(local_audio_path)
        web_audio_url = f"/static/audio/{filename}"

    return ProcessResponse(
        response=result.get("response", "System operational."),
        action=result.get("action", "none"),
        tts_audio_url=web_audio_url
    )