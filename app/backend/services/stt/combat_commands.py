"""Combat command parser — maps spoken enemy + direction to keyboard output."""

import time
import logging

logger = logging.getLogger("CombatCommands")

try:
    import pydirectinput
except ImportError:
    pydirectinput = None
    logger.warning("pydirectinput not available. Combat commands will be logged only.")

ENEMY_COMBOS = {
    "Bat": "Hit → Hit",
    "Slime": "Single Hit",
    "Skeleton": "Single Hit",
    "Zombie": "Single Hit",
    "Ghost": "Single Hit",
    "Mimic": "Single Hit",
    "Witch": "Single Hit",
    "Imp": "Single Hit",
    "Armored Skeleton": "Hit + Offbeat Hit",
    "Shielded Zombie": "Hit + Offbeat Hit",
    "Fast Bat": "Hit → Hit → Hit",
    "Split Slime": "Hit → Kill Spawned Enemies",
    "Exploder": "Single Hit",
    "Chain Enemy": "Hold → Release",
    "Teleporting Ghost": "Single Hit",
    "Rhythm Mage": "Single Hit",
    "Projectile Caster": "Single Hit",
    "Shield Bearer": "Hit + Offbeat Hit",
    "Dash Enemy": "Single Hit",
    "Boss Entity": "Special Pattern",
}

DIRECTIONS = {"left": "left", "right": "right", "up": "up", "down": "down"}

# Map combo actions to key sequences
_COMBO_KEYS = {
    "Single Hit": ["space"],
    "Hit → Hit": ["space", "space"],
    "Hit → Hit → Hit": ["space", "space", "space"],
    "Hit + Offbeat Hit": ["space", "shift"],
    "Hit → Kill Spawned Enemies": ["space", "space"],
    "Hold → Release": ["space"],  # hold handled via press/release below
    "Special Pattern": ["space", "shift", "space"],
}


def parse_command(text: str):
    """Parse transcribed text for an enemy name + optional direction.

    Returns (enemy, combo, direction) or None if no match.
    """
    lower = text.lower().strip()

    # Detect direction
    direction = None
    for word, key in DIRECTIONS.items():
        if word in lower:
            direction = key
            break

    # Match enemy (longest match first to handle multi-word names)
    matched_enemy = None
    for name in sorted(ENEMY_COMBOS, key=len, reverse=True):
        if name.lower() in lower:
            matched_enemy = name
            break

    if not matched_enemy:
        return None

    combo = ENEMY_COMBOS[matched_enemy]
    return matched_enemy, combo, direction


def execute_combat(enemy: str, direction: str | None):
    """Output direction key + combo keys via keyboard."""
    if not pydirectinput:
        logger.info(f"[dry-run] combat: {enemy} dir={direction}")
        return

    combo = ENEMY_COMBOS[enemy]

    if direction:
        pydirectinput.press(direction)

    if combo == "Hold → Release":
        pydirectinput.keyDown("space")
        time.sleep(0.3)
        pydirectinput.keyUp("space")
    else:
        for key in _COMBO_KEYS.get(combo, ["space"]):
            pydirectinput.press(key)
            time.sleep(0.05)
