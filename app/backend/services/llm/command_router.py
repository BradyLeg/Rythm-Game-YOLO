import os
import json
import logging
from openai import OpenAI
from app.backend.services.input.keyboard_handler import KeyboardHandler

logger = logging.getLogger("CommandRouter")

class CommandRouter:
    def __init__(self):
        # Pointing to your local gpt-oss-20b server instance
        self.client = OpenAI(
            base_url=os.getenv("LLM_BASE_URL", "http://localhost:11434/v1"),
            api_key="local-machine"
        )
        self.model_name = "gpt-oss:20b"
        
        # Instantiate your mapped dependency folder
        self.keyboard_handler = KeyboardHandler()

    def _get_tool_schema(self) -> list:
        """Defines the rigid schema to force tool usage selection on the LLM."""
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
        """
        Ingests natural speech text, handles LLM prompt constraints,
        and dispatches valid actions to the input handler.
        """
        system_prompt = (
            "You are an interactive AI assistant layer built into a rhythm game interface. "
            "Interpret voice transcripts efficiently. You must select the single most appropriate "
            "game tool function matching the user intent. Set reasoning effort to low."
        )

        try:
            # Execute inference with strict tool constraints
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_transcription}
                ],
                tools=self._get_tool_schema(),
                tool_choice={"type": "function", "function": {"name": "route_game_command"}},
                timeout=5.0
            )

            # Unpack tool call structural arguments
            tool_call = response.choices[0].message.tool_calls[0]
            arguments = json.loads(tool_call.function.arguments)
            
            action = arguments.get("action", "none")
            response_text = arguments.get("spoken_feedback", "")

            # Execute the routing phase to your input folder logic
            if action != "none":
                self.keyboard_handler.press_action_key(action)
            else:
                logger.info("🤖 [LLM Service] Command interpreted as informational. No routing required.")

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