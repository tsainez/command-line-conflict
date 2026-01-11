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

        # Security: Prevent path traversal and loading of unauthorized file types
        abs_path = os.path.abspath(target_path)

        # 1. Check extensions (whitelist)
        valid_extensions = {".ogg", ".wav", ".mp3"}
        _, ext = os.path.splitext(abs_path)
        if ext.lower() not in valid_extensions:
            log.warning(f"Security Alert: Attempted to load invalid music file type: {filepath}")
            return

        # 2. Check path traversal (must be within project or package root)
        project_root = os.path.abspath(os.getcwd())
        package_root = os.path.dirname(os.path.abspath(__file__))

        allowed_roots = [project_root, package_root]
        is_allowed = False

        for root in allowed_roots:
            try:
                # Use commonpath to ensure the file is contained within the root
                if os.path.commonpath([root, abs_path]) == root:
                    is_allowed = True
                    break
            except ValueError:
                continue

        if not is_allowed:
            log.warning(f"Security Alert: Attempted path traversal in music loading: {filepath}")
            return

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
