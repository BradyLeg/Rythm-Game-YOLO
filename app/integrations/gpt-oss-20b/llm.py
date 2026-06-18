import os
import json
from openai import OpenAI

class GPTOSS20BClient:
    def __init__(self):
        # Points to your local Ollama / llama.cpp instance
        self.client = OpenAI(
            base_url=os.getenv("LLM_BASE_URL", "http://localhost:11434/v1"),
            api_key="local-machine"
        )
        self.model_name = "gpt-oss:20b"

    def generate_response(self, user_transcription: str) -> dict:
        # Define the rhythm game tool schemas
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "game_action",
                    "description": "Trigger an in-game movement or navigation command.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "action": {
                                "type": "string",
                                "enum": ["move_up", "select", "go_back", "start_game", "none"]
                            },
                            "spoken_feedback": {
                                "type": "string",
                                "description": "What the MIKU voice should say back to the user."
                            }
                        },
                        "required": ["action", "spoken_feedback"]
                    }
                }
            }
        ]

        system_prompt = (
            "You are a rhythm-game voice assistant. Interpret user commands accurately. "
            "Always respond using the game_action tool. Set your reasoning effort to low "
            "for near-instant responses."
        )

        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_transcription}
                ],
                tools=tools,
                tool_choice={"type": "function", "function": {"name": "game_action"}},
                timeout=5.0  # Crucial for rhythm game responsiveness
            )

            # Extract tool arguments
            tool_call = response.choices[0].message.tool_calls[0]
            arguments = json.loads(tool_call.function.arguments)
            
            return {
                "action": arguments.get("action", "none"),
                "response": arguments.get("spoken_feedback", "")
            }

        except Exception as e:
            # Graceful fallback error handling (Task 2 requirements)
            return {
                "action": "none",
                "response": "Sorry, my systems lagged for a second.",
                "error": str(e)
            }