# test_complete_backend.py
import sys
import os
import logging

project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

logging.basicConfig(level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("whisper").setLevel(logging.WARNING)

from app.backend.orchestrator import GameOrchestrator

def run_test():
    print("=========================================================")
    print("🎤 RUNNING PACKAGED ORCHESTRATOR INTEGRATION")
    print("=========================================================\n")
    
    pipeline = GameOrchestrator()
    
    print("\n--- [Test Scenario: Live Mic Stream Execution] ---")
    print("Speak clearly into your mic when 'LISTENING' appears...")
    payload = pipeline.run_live_voice_pipeline(record_duration=4.0)
    
    print("\nFinal Returned Package Lifecycle Summary:")
    import pprint
    pprint.pprint(payload)

if __name__ == "__main__":
    run_test()