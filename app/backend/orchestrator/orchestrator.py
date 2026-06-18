import os
import logging
import threading
from app.backend.services.stt.mic_capture import record_audio
from app.integrations.whisper.stt import transcribe
from app.backend.services.llm.command_router import CommandRouter
from app.integrations.miku_tts.tts import MikuTTSClient

logger = logging.getLogger("Orchestrator")

class GameOrchestrator:
    def __init__(self):
        logger.info("Initializing Master Game Orchestration Pipeline...")
        self.command_router = CommandRouter()
        self.tts_client = MikuTTSClient()

    def handle_raw_text(self, text: str) -> dict:
        """Processes a plain text string through the routing and speech engines."""
        if not text or not text.strip():
            return {"action": "none", "response": "I didn't catch that.", "audio_path": ""}

        logger.info(f"⚡ [Orchestrator] Processing text input: '{text}'")
        
        # 1. Run text through LLM and execute hardware keystroke
        routing_result = self.command_router.process_and_route(text)
        action = routing_result.get("action", "none")
        spoken_response = routing_result.get("response", "")

        # 2. Synthesize Miku voice track response (fire-and-forget to avoid blocking)
        audio_file_path = ""
        if spoken_response:
            threading.Thread(
                target=self._generate_tts, args=(spoken_response,), daemon=True
            ).start()

        return {
            "action": action,
            "response": spoken_response,
            "audio_path": ""
        }

    def _generate_tts(self, text: str):
        """Background TTS generation — plays audio when ready."""
        try:
            self.tts_client.speak(text)
        except Exception as e:
            logger.error(f"❌ [Orchestrator] Miku TTS generation failed: {e}")

    def run_live_voice_pipeline(self, record_duration: float = 4.0) -> dict:
        """
        Records the microphone, transcribes with Whisper, and executes the core pipeline.
        Cleans up its own temporary user wav data automatically.
        """
        audio_capture_path = None
        try:
            logger.info(f"🛑 [Orchestrator] LISTENING... Speak your command ({record_duration}s)...")
            audio_capture_path = record_audio(duration_sec=record_duration)
            
            # Use your whisper.py script to turn the voice asset into a text string
            user_text = transcribe(audio_capture_path)
            logger.info(f"🗣️ [Orchestrator] Whisper Transcribed: \"{user_text}\"")

            if not user_text:
                return {"status": "silent", "action": "none", "response": "", "audio_path": ""}

            pipeline_result = self.handle_raw_text(user_text)
            pipeline_result["status"] = "success"
            pipeline_result["transcription"] = user_text
            return pipeline_result

        except Exception as e:
            logger.error(f"❌ [Orchestrator] Voice lifecycle broke: {e}")
            return {"status": "error", "message": str(e), "action": "none", "response": "", "audio_path": ""}
            
        finally:
            if audio_capture_path and os.path.exists(audio_capture_path):
                try:
                    os.remove(audio_capture_path)
                except Exception:
                    pass