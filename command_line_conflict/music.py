import os
import pygame
from . import config
from .logger import log

class MusicManager:
    """Manages background music playback."""

    def __init__(self):
        """Initializes the MusicManager."""
        self.enabled = config.MUSIC_ENABLED
        self.volume = config.MUSIC_VOLUME
        self.current_track = None

        if not pygame.mixer.get_init():
             try:
                 pygame.mixer.init()
             except pygame.error as e:
                 log.error(f"Failed to initialize pygame mixer: {e}")
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

        if not os.path.exists(filepath):
            log.warning(f"Music file not found: {filepath}")
            return

        try:
            pygame.mixer.music.load(filepath)
            pygame.mixer.music.play(loop)
            self.current_track = filepath
            log.info(f"Playing music: {filepath}")
        except pygame.error as e:
            log.error(f"Failed to play music {filepath}: {e}")

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
            pygame.mixer.music.set_volume(self.volume)
