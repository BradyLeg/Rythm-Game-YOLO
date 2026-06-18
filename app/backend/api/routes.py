from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


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
    return ProcessResponse(
        response=f"Received: {req.text}",
        action="none",
        tts_audio_url="",
    )
