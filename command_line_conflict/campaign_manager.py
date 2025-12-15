import json
import os
from pathlib import Path
from typing import Dict, List, Set

from .logger import log

SAVE_FILE = "save_game.json"

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

MISSIONS = [
    {
        "id": "mission_1",
        "title": "Mission 1: First Contact",
        "briefing": "Commander, we have established a foothold on the surface. Enemy rovers have been detected in the sector. Your orders are to eliminate all hostile threats. Our scanners indicate a small scout force. Do not let them report back.",
        "unlocks": ["rover"],
    },
    {
        "id": "mission_2",
        "title": "Mission 2: Escalation",
        "briefing": "The enemy knows we are here. They have deployed Arachnotrons to counter our ground forces. We are authorizing the production of Arachnotrons to combat this aerial threat. Secure the area.",
        "unlocks": ["arachnotron"],
    },
    {
        "id": "mission_3",
        "title": "Mission 3: The Eye in the Sky",
        "briefing": "We need better intelligence. The enemy is moving in the shadows. We are unlocking the Observer schematic. Use it to scout ahead and reveal cloaked units. Eliminate the enemy base.",
        "unlocks": ["observer"],
    },
    {
        "id": "mission_4",
        "title": "Mission 4: Heavy Metal",
        "briefing": "It's time to finish this. We are deploying the Immortal. This heavy assault walker will crush their defenses. Destroy their main command center. Victory is at hand.",
        "unlocks": ["immortal"],
    },
]


class CampaignManager:
    """Manages campaign progress, including completed missions and unlocked units."""

    def __init__(self, save_file: str = SAVE_FILE):
        self.save_file = save_file
        self.completed_missions: List[str] = []
        self.unlocked_units: Set[str] = {"chassis", "extractor"}  # Default unlocks
        self.load_progress()

    def load_progress(self) -> None:
        """Loads progress from the save file."""
        if not os.path.exists(self.save_file):
            log.info("No save file found. Starting new campaign.")
            return

        try:
            with open(self.save_file, "r") as f:
                data = json.load(f)
                self.completed_missions = data.get("completed_missions", [])
                # Re-evaluate unlocks based on completed missions
                self._update_unlocks()
                log.info(
                    f"Loaded campaign progress: {len(self.completed_missions)} missions completed."
                )
        except Exception as e:
            log.error(f"Failed to load save file: {e}")

    def save_progress(self) -> None:
        """Saves current progress to the save file."""
        data = {
            "completed_missions": self.completed_missions,
        }
        try:
            with open(self.save_file, "w") as f:
                json.dump(data, f, indent=4)
            log.info("Campaign progress saved.")
        except Exception as e:
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

    def get_mission(self, mission_id: str) -> dict:
        """Retrieves mission metadata by ID.

        Args:
            mission_id: The ID of the mission.

        Returns:
            The mission dictionary, or None if not found.
        """
        for mission in MISSIONS:
            if mission["id"] == mission_id:
                return mission
        return None

    def get_all_missions(self) -> List[dict]:
        """Returns a list of all defined missions."""
        return MISSIONS

    def is_mission_unlocked(self, mission_id: str) -> bool:
        """Checks if a mission is unlocked (previous mission completed)."""
        if mission_id == "mission_1":
            return True

        # Find index
        idx = -1
        for i, m in enumerate(MISSIONS):
            if m["id"] == mission_id:
                idx = i
                break

        if idx > 0:
            prev_mission_id = MISSIONS[idx - 1]["id"]
            return prev_mission_id in self.completed_missions

        return False
