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

        # Security: Reject non-regular files and oversized inputs to avoid DoS or special file abuse
        if not os.path.isfile(target_path):
            log.warning(f"Music file must be a regular file: {target_path}")
            return
        try:
            size = os.path.getsize(target_path)
        except OSError as e:
            log.warning(f"Unable to read music file size ({target_path}): {e}")
            return
        if size > config.MAX_AUDIO_FILE_SIZE:
            log.warning("Music file %s exceeds maximum allowed size (%s bytes)", target_path, config.MAX_AUDIO_FILE_SIZE)
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
