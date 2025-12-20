"""Steamworks integration for Command Line Conflict."""

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
        except Exception as e:
            log.warning(f"Failed to initialize Steamworks: {e}")

    def unlock_achievement(self, achievement_name: str) -> None:
        """Unlocks a Steam achievement.

        Args:
            achievement_name: The API name of the achievement to unlock.
        """
        if not self.initialized or not self.steam:
            log.debug(f"Steam not initialized. Skipping achievement: {achievement_name}")
            return

        try:
            self.steam.SetAchievement(achievement_name)
            self.steam.StoreStats()
            log.info(f"Unlocked achievement: {achievement_name}")
        except Exception as e:
            log.error(f"Failed to unlock achievement {achievement_name}: {e}")

    def update(self) -> None:
        """Runs Steam callbacks. Should be called every frame."""
        if self.initialized and self.steam:
            try:
                self.steam.RunCallbacks()
            except Exception:
                pass
