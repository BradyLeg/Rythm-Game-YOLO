import os
import uuid
import logging
import shutil
from gradio_client import Client

logger = logging.getLogger("MikuTTS")
logging.basicConfig(level=logging.INFO)

class MikuTTSClient:
    def __init__(self):
        # Pointing directly to John6666's live Miku TTS Gradio Space
        self.space_id = "John6666/mikuTTS"
        
        # Directory where generated game audio assets will reside
        self.output_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../../../app/backend/static/audio")
        )
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Lazy load client to prevent slowing down server startup when offline
        self._client = None

    @property
    def client(self):
        if self._client is None:
            logger.info(f"🌐 Connecting to Hugging Face Space: {self.space_id}...")
            # Handshake with Hugging Face Space
            self._client = Client(self.space_id)
        return self._client

    def speak(self, text: str) -> str:
        """
        Sends text to John6666's Hugging Face Miku TTS space.
        Saves the authentic RVC output track and returns the local file path.
        """
        if not text:
            return ""

        unique_filename = f"miku_{uuid.uuid4().hex[:10]}.wav"
        final_file_path = os.path.join(self.output_dir, unique_filename)

        logger.info(f"🎤 [TTS Service] Generating Miku voice line for: '{text}'")

        try:
            # pass all 10 expected values matching the explicit API signature positions
            outputs = self.client.predict(
                model_name="1a_miku_default_rvc_(aple)", # Parameter 1: Selects Miku's RVC weights
                speed=0,                                 # Parameter 2: Default speaking rate
                volume=0,                                # Parameter 3: Default baseline gain
                pitch=0,                                 # Parameter 4: Keyshift adjustments
                tts_text=text,                           # Parameter 5: The actual line for Miku to say
                tts_voice="en-US-AvaNeural-Female",      # Parameter 6: Clean English edge base voice
                f0_up_key=6,                             # Parameter 7: Default pitch lift parameter
                f0_method="rmvpe",                       # Parameter 8: Highest quality pitch extraction
                index_rate=1,                            # Parameter 9: Voice blend index control
                protect=0.33,                            # Parameter 10: Protect voiceless consonants
                api_name="/tts"                          # Point directly to the explicit /tts endpoint
            )
            
            # The API returns a tuple/list: (output_info, edge_voice, result)
            # Index 2 contains the final, high-fidelity RVC-converted Miku audio asset
            temp_audio_path = outputs[2] if isinstance(outputs, (list, tuple)) else outputs

            if temp_audio_path and os.path.exists(temp_audio_path):
                shutil.move(temp_audio_path, final_file_path)
                logger.info(f"✨ [TTS Service] Audio captured successfully: {final_file_path}")
                return final_file_path
            
        except Exception as e:
            logger.error(f"❌ [TTS Service] Hugging Face Space inference failed or timed out: {e}")
        
        return self._generate_fallback_audio(text, final_file_path)

    def _generate_fallback_audio(self, text: str, fallback_path: str) -> str:
        logger.warning("⚠️ [TTS Fallback] Falling back to local system synthesizer.")
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.save_to_file(text, fallback_path)
            engine.runAndWait()
            return fallback_path
        except ImportError:
            logger.warning("pyttsx3 not available. Skipping fallback generation.")
            return ""