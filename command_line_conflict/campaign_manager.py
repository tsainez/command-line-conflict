import json
import os
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Set

from .logger import log
from .utils.paths import get_user_data_dir

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

    def __init__(self, save_file: Optional[str] = None):
        if save_file:
            self.save_file = save_file
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

        try:
            with open(self.save_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.completed_missions = data.get("completed_missions", [])
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
            with open(self.save_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            log.info("Campaign progress saved.")
        except IOError as e:
            log.error(f"Failed to save progress: {e}")

    def complete_mission(self, mission_id: str) -> None:
        """Marks a mission as completed and saves progress.

        Args:
            mission_id: The unique identifier of the completed mission.
        """
        if mission_id not in self.completed_missions:
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
