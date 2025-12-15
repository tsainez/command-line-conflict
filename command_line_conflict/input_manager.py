import json
import os
import pygame
from .logger import log

DEFAULT_BINDINGS = {
    "camera_up": pygame.K_UP,
    "camera_down": pygame.K_DOWN,
    "camera_left": pygame.K_LEFT,
    "camera_right": pygame.K_RIGHT,
    "build_rover_factory": pygame.K_r,
    "build_arachnotron_factory": pygame.K_a,
    "hold_position": pygame.K_h,
    "pause": pygame.K_p,
    "toggle_reveal_map": pygame.K_F1,
    "toggle_god_mode": pygame.K_F2,
    "switch_player": pygame.K_TAB,
    "menu": pygame.K_ESCAPE,
    "spawn_extractor": pygame.K_1,
    "spawn_chassis": pygame.K_2,
    "spawn_rover": pygame.K_3,
    "spawn_arachnotron": pygame.K_4,
    "spawn_observer": pygame.K_5,
    "spawn_immortal": pygame.K_6,
}

BINDINGS_FILE = "keybindings.json"


class InputManager:
    """Manages keybindings for the game."""

    def __init__(self):
        self.bindings = DEFAULT_BINDINGS.copy()
        self.load_bindings()

    def load_bindings(self):
        """Loads keybindings from a file."""
        if os.path.exists(BINDINGS_FILE):
            try:
                with open(BINDINGS_FILE, "r") as f:
                    loaded = json.load(f)
                    # Merge loaded bindings with defaults to ensure new keys are present
                    for key, val in loaded.items():
                        if key in self.bindings:
                            self.bindings[key] = val
                log.info("Keybindings loaded.")
            except Exception as e:
                log.error(f"Failed to load keybindings: {e}")

    def save_bindings(self):
        """Saves current keybindings to a file."""
        try:
            with open(BINDINGS_FILE, "w") as f:
                json.dump(self.bindings, f, indent=4)
            log.info("Keybindings saved.")
        except Exception as e:
            log.error(f"Failed to save keybindings: {e}")

    def get_key(self, action):
        """Returns the key code for a given action."""
        return self.bindings.get(action, DEFAULT_BINDINGS.get(action))

    def set_key(self, action, key_code):
        """Sets the key code for a given action and saves."""
        self.bindings[action] = key_code
        self.save_bindings()
