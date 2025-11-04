import json

SAVE_FILE = "save_game.json"

def save_game(mission_number):
    """Saves the player's current mission number.
    Args:
        mission_number: The mission number to save.
    """
    with open(SAVE_FILE, "w") as f:
        json.dump({"mission_number": mission_number}, f)

def load_game():
    """Loads the player's current mission number.
    Returns:
        The mission number, or 1 if no save file exists.
    """
    try:
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
            return data.get("mission_number", 1)
    except FileNotFoundError:
        return 1
