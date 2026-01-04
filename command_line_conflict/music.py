import os

import pygame

from . import config
from .logger import log
from .utils.audio import init_mixer


class MusicManager:
    """Manages background music playback."""

    def __init__(self):
        """Initializes the MusicManager."""
        self.enabled = config.MUSIC_ENABLED
        self.volume = config.MUSIC_VOLUME
        self.current_track = None

        if not init_mixer():
            self.enabled = False

        if self.enabled:
            try:
                pygame.mixer.music.set_volume(self.volume)
            except pygame.error:
                pass

    def play(self, filepath, loop=-1):
        """Plays a music file.

        Args:
            filepath: Path to the music file.
            loop: Number of times to loop the music. -1 means infinite loop.
        """
        if not self.enabled:
            return

        if self.current_track == filepath:
            if pygame.mixer.music.get_busy():
                return

        # Check if file exists, or try extensions if none provided
        target_path = filepath
        if not os.path.exists(target_path):
            # If path doesn't exist, try appending extensions
            for ext in [".ogg", ".wav", ".mp3"]:
                if os.path.exists(target_path + ext):
                    target_path = target_path + ext
                    break

        if not os.path.exists(target_path):
            log.warning(f"Music file not found: {filepath}")
            return

        try:
            pygame.mixer.music.load(target_path)
            pygame.mixer.music.play(loop)
            self.current_track = target_path
            log.info(f"Playing music: {target_path}")
        except pygame.error as e:
            log.error(f"Failed to play music {target_path}: {e}")

    def stop(self):
        """Stops the currently playing music."""
        if self.enabled:
            pygame.mixer.music.stop()
            self.current_track = None

    def set_volume(self, volume):
        """Sets the music volume.

        Args:
            volume: A float between 0.0 and 1.0.
        """
        self.volume = max(0.0, min(1.0, volume))
        if self.enabled:
            pygame.mixer.music.set_volume(self.volume * config.MASTER_VOLUME)

    def refresh_volume(self):
        """Refreshes the music volume based on the master volume."""
        self.set_volume(self.volume)
