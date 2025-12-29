import os

import pygame

from command_line_conflict import config
from command_line_conflict.logger import log


class SoundSystem:
    """Manages sound effects playback."""

    def __init__(self):
        """Initializes the SoundSystem."""
        self.enabled = config.SOUND_ENABLED
        self.volume = config.SOUND_VOLUME
        self.sounds = {}

        if not pygame.mixer.get_init():
            try:
                pygame.mixer.init()
            except pygame.error as e:
                log.error(f"Failed to initialize pygame mixer: {e}")
                self.enabled = False

    def update(self, game_state):
        """Processes sound events from the game state.

        Args:
            game_state: The current game state.
        """
        if not self.enabled:
            return

        for event in game_state.event_queue:
            if event.get("type") == "sound":
                sound_name = event["data"].get("name")
                self.play_sound(sound_name)

    def play_sound(self, name):
        """Plays a sound effect.

        Args:
            name: The name of the sound file (without extension).
        """
        if not self.enabled:
            return

        if name not in self.sounds:
            self._load_sound(name)

        sound = self.sounds.get(name)
        if sound:
            try:
                sound.play()
            except pygame.error as e:
                log.error(f"Failed to play sound {name}: {e}")

    def _load_sound(self, name):
        """Loads a sound file into memory.

        Args:
            name: The name of the sound file.
        """
        # Calculate path relative to this file
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        sounds_dir = os.path.join(base_path, "sounds")

        # Try .wav first (user preference), then .ogg
        extensions = [".wav", ".ogg"]
        filepath = None

        for ext in extensions:
            path = os.path.join(sounds_dir, f"{name}{ext}")

            # Security: Prevent path traversal
            # Resolve the absolute path
            abs_path = os.path.abspath(path)

            # Ensure the resolved path starts with the sounds directory
            # We use commonpath to correctly handle directory boundaries and avoid prefix matching issues
            # e.g. /app/sounds_confidential would match startswith('/app/sounds') but not commonpath
            try:
                if os.path.commonpath([abs_path, os.path.abspath(sounds_dir)]) != os.path.abspath(sounds_dir):
                    log.warning(f"Security Alert: Attempted path traversal in sound loading: {name}")
                    self.sounds[name] = None
                    return
            except ValueError:
                # commonpath raises ValueError if paths are on different drives (Windows)
                log.warning(f"Security Alert: Attempted cross-drive access in sound loading: {name}")
                self.sounds[name] = None
                return

            if os.path.exists(abs_path):
                filepath = abs_path
                break

        if not filepath:
            # Log warning only once per sound to avoid spam
            if name not in self.sounds:
                log.warning(f"Sound file not found: {name} (checked .wav, .ogg)")
                self.sounds[name] = None  # Cache failure to avoid repeated checks
            return

        try:
            sound = pygame.mixer.Sound(filepath)
            sound.set_volume(self.volume * config.MASTER_VOLUME)
            self.sounds[name] = sound
        except pygame.error as e:
            log.error(f"Failed to load sound {filepath}: {e}")
            self.sounds[name] = None
