"""Steamworks integration for Command Line Conflict."""

import re

from .logger import log


class SteamIntegration:
    """Manages Steamworks integration for achievements and other features."""

    def __init__(self):
        """Initializes the SteamIntegration."""
        self.steam = None
        self.initialized = False

        try:
            # Try to import steamworks (SteamworksPy)
            # The package is usually 'steamworks'
            import steamworks

            self.steam = steamworks.STEAMWORKS()
            self.steam.initialize()
            self.initialized = True
            log.info("Steamworks initialized successfully.")
        except ImportError:
            log.warning("steamworks module not found. Steam integration disabled.")
        except Exception as e:  # pylint: disable=broad-exception-caught
            log.warning(f"Failed to initialize Steamworks: {e} ({type(e).__name__})")

    def unlock_achievement(self, achievement_name: str) -> None:
        """Unlocks a Steam achievement.

        Args:
            achievement_name: The API name of the achievement to unlock.
        """
        # Security: Validate achievement_name to prevent injection or DoS
        if not achievement_name or len(achievement_name) > 64:
            log.warning(f"Invalid achievement name length: {achievement_name}")
            return

        if not re.match(r"^[A-Za-z0-9_]+$", achievement_name):
            log.warning(f"Invalid achievement name format: {achievement_name}")
            return

        if not self.initialized or not self.steam:
            log.debug(f"Steam not initialized. Skipping achievement: {achievement_name}")
            return

        # Security check: Validate achievement_name to prevent injection or crashes
        # Allow only alphanumeric characters and underscores, max 64 characters
        if (
            not isinstance(achievement_name, str)
            or len(achievement_name) > 64
            or not re.match(r"^[A-Za-z0-9_]+$", achievement_name)
        ):
            log.warning(f"Security Warning: Invalid achievement name format rejected: {achievement_name}")
            return

        try:
            self.steam.SetAchievement(achievement_name)
            self.steam.StoreStats()
            log.info(f"Unlocked achievement: {achievement_name}")
        except Exception as e:  # pylint: disable=broad-exception-caught
            log.error(f"Failed to unlock achievement {achievement_name}: {e} ({type(e).__name__})")

    def update(self) -> None:
        """Runs Steam callbacks. Should be called every frame."""
        if self.initialized and self.steam:
            try:
                self.steam.RunCallbacks()
            except Exception:  # pylint: disable=broad-exception-caught
                pass
