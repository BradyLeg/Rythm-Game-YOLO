import os
import json
import logging
from openai import OpenAI
from app.backend.services.input.keyboard_handler import KeyboardHandler

logger = logging.getLogger("CommandRouter")

class CommandRouter:
    def __init__(self):
        self.client = OpenAI(
            base_url=os.getenv("LLM_BASE_URL", "http://localhost:11434/v1"),
            api_key="local-machine"
        )
        self.model_name = "gpt-oss:20b"
        self.keyboard_handler = KeyboardHandler()

    def _get_tool_schema(self) -> list:
        return [
            {
                "type": "function",
                "function": {
                    "name": "route_game_command",
                    "description": "Route natural voice commands to physical rhythm-game actions.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "action": {
                                "type": "string",
                                "description": "CRITICAL: You must choose ONLY from this exact list.",
                                "enum": ["move_up", "move_down", "select", "go_back", "start_game", "none"]
                            },
                            "spoken_feedback": {
                                "type": "string",
                                "description": "Short, immersive phrase Miku will say back to the user."
                            }
                        },
                        "required": ["action", "spoken_feedback"]
                    }
                }
            }
        ]

    def process_and_route(self, user_transcription: str) -> dict:
        system_prompt = (
            "You are an interactive AI assistant layer built into a rhythm game interface.\n"
            "Interpret voice transcripts efficiently. You MUST invoke the 'route_game_command' tool.\n"
            "CRITICAL RULES:\n"
            "1. For the 'action' argument, you are strictly FORBIDDEN from generating strings outside the enum list.\n"
            "2. Map 'next song' or 'scroll up' directly to 'move_up'.\n"
            "3. Map 'return to menu' or 'go back' directly to 'go_back'.\n"
            "4. If the message is completely unrelated to game controls, use the action 'none'."
        )

        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_transcription}
                ],
                tools=self._get_tool_schema(),
                tool_choice={"type": "function", "function": {"name": "route_game_command"}},
                timeout=60.0
            )

            message = response.choices[0].message
            
            if not message.tool_calls:
                logger.info("🤖 [LLM Service] Model opted out of tool calling. Generating fallback response.")
                return {
                    "action": "none",
                    "response": message.content if message.content else "I'm not sure how to help with that in-game."
                }

            tool_call = message.tool_calls[0]
            arguments = json.loads(tool_call.function.arguments)
            
            action = arguments.get("action", "none")
            response_text = arguments.get("spoken_feedback", "")

            if action != "none":
                self.keyboard_handler.press_action_key(action)
            else:
                logger.info("🤖 [LLM Service] Intended action evaluates to 'none'.")

            return {
                "action": action,
                "response": response_text
            }

        except Exception as e:
            logger.error(f"Error handling orchestration chain: {e}")
            return {
                "action": "none",
                "response": "Processing error, keeping game state stable.",
                "error": str(e)
            }