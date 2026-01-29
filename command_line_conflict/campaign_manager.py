import json
import os
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Set

from .logger import log
from .utils.paths import atomic_save_json, get_user_data_dir

DEFAULT_SAVE_FILENAME = "save_game.json"

# Define the Tech Tree: Mission ID -> List of Unlocked Units
# Mission 1 unlocks Rover
# Mission 2 unlocks Arachnotron
# ...
MISSION_REWARDS: Dict[str, List[str]] = {
    "mission_1": ["rover"],
    "mission_2": ["arachnotron"],
    "mission_3": ["observer"],
    "mission_4": ["immortal"],
}


class CampaignManager:
    """Manages campaign progress, including completed missions and unlocked units."""

    MAX_SAVE_FILE_SIZE = 512 * 1024  # 512KB limit to prevent DoS
    MAX_MISSIONS_COUNT = 1000  # Limit number of missions to track
    MAX_MISSION_ID_LENGTH = 64  # Security limit for mission ID length

    def __init__(self, save_file: Optional[str] = None):
        if save_file:
            # Security fix: Enforce .json extension to prevent arbitrary file overwrite
            path = Path(save_file).resolve()
            if path.suffix.lower() != ".json":
                raise ValueError("Save file must have .json extension")
            self.save_file = str(path)
        else:
            data_dir = get_user_data_dir()
            try:
                data_dir.mkdir(parents=True, exist_ok=True)
            except OSError as e:
                log.error(f"Failed to create data directory {data_dir}: {e}")

            self.save_file = str(data_dir / DEFAULT_SAVE_FILENAME)

            # Check for legacy save file in current directory and migrate if needed
            legacy_file = Path(DEFAULT_SAVE_FILENAME)
            if legacy_file.exists() and not Path(self.save_file).exists():
                log.info(f"Migrating save file from {legacy_file} to {self.save_file}")
                try:
                    shutil.move(str(legacy_file), self.save_file)
                except OSError as e:
                    log.error(f"Failed to migrate save file: {e}")

        self.completed_missions: List[str] = []
        self.unlocked_units: Set[str] = {"chassis", "extractor"}  # Default unlocks
        self.load_progress()

    def load_progress(self) -> None:
        """Loads progress from the save file."""
        if not os.path.exists(self.save_file):
            log.info("No save file found. Starting new campaign.")
            return

        # Security check: File size
        # We perform this check when reading to prevent TOCTOU race conditions
        # where the file grows between check and read.
        try:
            with open(self.save_file, "r", encoding="utf-8") as f:
                # Read up to the limit + 1 char to detect overflow
                content = f.read(self.MAX_SAVE_FILE_SIZE + 1)

                if len(content) > self.MAX_SAVE_FILE_SIZE:
                    log.error(f"Failed to load save file: File exceeds maximum allowed size ({self.MAX_SAVE_FILE_SIZE} bytes)")
                    return

                if not content:
                    log.info("Save file is empty. Starting new campaign.")
                    return

                data = json.loads(content)

                # Security check: Validate structure and limits
                missions = data.get("completed_missions", [])
                if not isinstance(missions, list):
                    missions = []
                    log.warning("Invalid 'completed_missions' format, expected list. Resetting.")

                if len(missions) > self.MAX_MISSIONS_COUNT:
                    log.warning(f"Too many completed missions ({len(missions)}). Truncating to {self.MAX_MISSIONS_COUNT}.")
                    missions = missions[: self.MAX_MISSIONS_COUNT]

                # Ensure all entries are strings and within length limits
                self.completed_missions = []
                for m in missions:
                    m_str = str(m)
                    if len(m_str) <= self.MAX_MISSION_ID_LENGTH:
                        self.completed_missions.append(m_str)
                    else:
                        log.warning(f"Skipping mission ID exceeding length limit: {m_str[:20]}...")

                # Re-evaluate unlocks based on completed missions
                self._update_unlocks()
                log.info(f"Loaded campaign progress: {len(self.completed_missions)} missions completed.")
        except (IOError, json.JSONDecodeError) as e:
            log.error(f"Failed to load save file: {e}")

    def save_progress(self) -> None:
        """Saves current progress to the save file."""
        data = {
            "completed_missions": self.completed_missions,
        }
        try:
            # Security: Use atomic save to prevent data corruption
            atomic_save_json(self.save_file, data)
            log.info("Campaign progress saved.")
        except IOError as e:
            log.error(f"Failed to save progress: {e}")

    def complete_mission(self, mission_id: str) -> None:
        """Marks a mission as completed and saves progress.

        Args:
            mission_id: The unique identifier of the completed mission.
        """
        # Security check: Validate mission ID length
        if len(mission_id) > self.MAX_MISSION_ID_LENGTH:
            log.warning(
                f"Failed to complete mission: ID '{mission_id[:20]}...' exceeds maximum length of {self.MAX_MISSION_ID_LENGTH}"
            )
            return

        if mission_id not in self.completed_missions:
            # Security check: Validate max missions count
            if len(self.completed_missions) >= self.MAX_MISSIONS_COUNT:
                log.warning(
                    f"Failed to complete mission {mission_id}: Maximum mission count ({self.MAX_MISSIONS_COUNT}) reached."
                )
                return

            log.info(f"Mission {mission_id} completed!")
            self.completed_missions.append(mission_id)
            self._update_unlocks()
            self.save_progress()

    def _update_unlocks(self) -> None:
        """Updates the set of unlocked units based on completed missions."""
        self.unlocked_units = {"chassis", "extractor"}  # Reset to default
        for mission_id in self.completed_missions:
            rewards = MISSION_REWARDS.get(mission_id, [])
            for unit in rewards:
                self.unlocked_units.add(unit)
                log.info(f"Unlocked unit: {unit}")

    def is_unit_unlocked(self, unit_name: str) -> bool:
        """Checks if a specific unit is unlocked.

        Args:
            unit_name: The name of the unit (e.g., 'rover').

        Returns:
            True if the unit is unlocked, False otherwise.
        """
        return unit_name in self.unlocked_units
