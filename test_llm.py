import sys
import os

# Add the project root to your python path so imports resolve cleanly
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.backend.services.llm.command_router import CommandRouter

def run_smoke_test():
    print("🤖 Initializing CommandRouter and connecting to local gpt-oss:20b...")
    router = CommandRouter()
    
    # Test cases to see if the model handles different intents correctly
    test_prompts = [
        "Can you move up to the next song please?",
        "Go back to the main menu screen.",
        "Let's start the game!",
        "What is the weather like today?" # This should result in 'none' action
    ]
    
    print("\n--- Starting Test Sequence ---")
    for i, prompt in enumerate(test_prompts, 1):
        print(f"\n[Test {i}] User Said: '{prompt}'")
        
        # This will call the local model AND simulate the keypress if successful!
        result = router.process_and_route(prompt)
        
        print(f" -> Interpreted Action: {result.get('action')}")
        print(f" -> Miku's Response:   '{result.get('response')}'")
        if "error" in result:
            print(f" ❌ Error encountered: {result['error']}")

if __name__ == "__main__":
    run_smoke_test()