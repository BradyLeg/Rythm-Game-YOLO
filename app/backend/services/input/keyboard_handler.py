import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("KeyboardHandler")

try:
    import pydirectinput
    pydirectinput.PAUSE = 0.05
except ImportError:
    pydirectinput = None
    logger.warning("pydirectinput not found. Keyboard inputs will be simulated via dry-run logs.")

class KeyboardHandler:
    def __init__(self):
        # A clean map matching structural action intent to standard keyboard layout
        self.key_map = {
            "move_up": "up",
            "move_down": "down",
            "select": "enter",
            "go_back": "escape",
            "start_game": "space"
        }

    def press_action_key(self, action_intent: str) -> bool:
        """Translates an abstract intent into a direct physical keypress."""
        target_key = self.key_map.get(action_intent)
        
        if not target_key:
            logger.warning(f"No key mapping established for intent: '{action_intent}'")
            return False

        logger.info(f"⌨️ [Input Service] Emulating keypress: [{target_key.upper()}] for intent '{action_intent}'")
        
        if pydirectinput:
            try:
                pydirectinput.press(target_key)
                return True
            except Exception as e:
                logger.error(f"Hardware simulation error pressing {target_key}: {e}")
                return False
        return True