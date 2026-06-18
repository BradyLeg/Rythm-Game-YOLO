import sys
import os

# Ensure the root path is verified
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from app.integrations.miku_tts.tts import MikuTTSClient

def run_tts_test():
    print("🎤 Initializing MikuTTS Client and checking connection...")
    tts = MikuTTSClient()
    
    test_line = "Got it! Moving to the next track!"
    print(f"\nSending line to Miku: '{test_line}'")
    
    audio_path = tts.speak(test_line)
    
    if audio_path and os.path.exists(audio_path):
        print(f"✅ Success! Voice asset created at: {audio_path}")
        print("Go check that folder and play it to hear Miku!")
    else:
        print("❌ Failed to generate audio asset.")

if __name__ == "__main__":
    run_tts_test()