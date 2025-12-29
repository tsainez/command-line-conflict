import json
import os
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Set, Any

from .logger import log
from .utils.paths import get_user_data_dir
from .tech_tree import TECH_TREE, MISSION_CHOICES, TechNode

DEFAULT_SAVE_FILENAME = "save_game.json"

class CampaignManager:
    """Manages campaign progress, including completed missions and unlocked tech."""

    MAX_SAVE_FILE_SIZE = 512 * 1024  # 512KB limit to prevent DoS
    MAX_MISSIONS_COUNT = 1000  # Limit number of missions to track
    MAX_MISSION_ID_LENGTH = 64  # Security limit for mission ID length
    MAX_TECH_ID_LENGTH = 64 # Security limit for tech ID

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
        self.unlocked_techs: Set[str] = set()

        # Determine unlocked units from techs
        self.unlocked_units: Set[str] = {"chassis", "extractor"}

        self.load_progress()

    def load_progress(self) -> None:
        """Loads progress from the save file."""
        if not os.path.exists(self.save_file):
            log.info("No save file found. Starting new campaign.")
            # Default unlocks
            self.unlocked_techs = set()
            # Note: We might want to give default techs here if any
            return

        # Security check: File size
        try:
            if os.path.getsize(self.save_file) > self.MAX_SAVE_FILE_SIZE:
                log.error(f"Failed to load save file: File exceeds maximum allowed size ({self.MAX_SAVE_FILE_SIZE} bytes)")
                return
        except OSError as e:
            log.error(f"Failed to check save file size: {e}")
            return

        try:
            with open(self.save_file, "r", encoding="utf-8") as f:
                data = json.load(f)

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

                # Load Techs
                techs = data.get("unlocked_techs", [])
                if not isinstance(techs, list):
                     # Migration from legacy save (which didn't have unlocked_techs)
                    log.info("Migrating legacy save to tech tree system.")
                    self._migrate_legacy_unlocks(missions)
                else:
                    self.unlocked_techs = set()
                    for t in techs:
                        t_str = str(t)
                        if len(t_str) <= self.MAX_TECH_ID_LENGTH:
                            if t_str in TECH_TREE:
                                self.unlocked_techs.add(t_str)
                            else:
                                log.warning(f"Skipping unknown tech ID: {t_str}")
                        else:
                             log.warning(f"Skipping tech ID exceeding length limit: {t_str[:20]}...")

                self._refresh_derived_state()
                log.info(f"Loaded campaign progress: {len(self.completed_missions)} missions completed, {len(self.unlocked_techs)} techs unlocked.")

        except (IOError, json.JSONDecodeError) as e:
            log.error(f"Failed to load save file: {e}")

    def _migrate_legacy_unlocks(self, completed_missions: List[str]):
        """Migrates legacy mission-based unlocks to tech tree nodes."""
        self.unlocked_techs = set()

        # Hardcoded legacy mapping
        legacy_mapping = {
            "mission_1": ["unlock_rover"],
            "mission_2": ["unlock_arachnotron"],
            "mission_3": ["unlock_observer"],
            "mission_4": ["unlock_immortal"],
        }

        for mission_id in completed_missions:
            techs = legacy_mapping.get(mission_id, [])
            for t in techs:
                if t in TECH_TREE:
                    self.unlocked_techs.add(t)

    def _refresh_derived_state(self):
        """Updates derived state like unlocked_units from unlocked_techs."""
        self.unlocked_units = {"chassis", "extractor"}
        for tech_id in self.unlocked_techs:
            tech = TECH_TREE.get(tech_id)
            if tech and tech.type == "unit":
                # Find unit_id in modifiers
                for mod in tech.modifiers:
                    if mod.get("stat") == "unlock" and mod.get("value") is True:
                        self.unlocked_units.add(mod.get("unit_id"))

    def save_progress(self) -> None:
        """Saves current progress to the save file."""
        data = {
            "completed_missions": self.completed_missions,
            "unlocked_techs": list(self.unlocked_techs)
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
            # Note: We do NOT automatically unlock things anymore.
            # The player must choose rewards.
            # But we should save the fact that the mission is done.
            self.save_progress()

    def unlock_tech(self, tech_id: str) -> bool:
        """Unlocks a specific tech node.

        Args:
            tech_id: The ID of the tech to unlock.

        Returns:
            True if successful, False if invalid or requirements not met.
        """
        if tech_id not in TECH_TREE:
            log.warning(f"Attempted to unlock unknown tech: {tech_id}")
            return False

        tech = TECH_TREE[tech_id]

        # Check prerequisites
        for req in tech.prerequisites:
            if req not in self.unlocked_techs:
                log.warning(f"Cannot unlock {tech_id}: Prerequisite {req} missing.")
                return False

        # Check mutual exclusion
        for conflict in tech.mutually_exclusive_with:
            if conflict in self.unlocked_techs:
                log.warning(f"Cannot unlock {tech_id}: Conflict with {conflict}.")
                return False

        self.unlocked_techs.add(tech_id)
        self._refresh_derived_state()
        self.save_progress()
        log.info(f"Unlocked tech: {tech_id}")
        return True

    def get_available_choices(self, mission_id: str) -> List[TechNode]:
        """Returns a list of TechNodes available as rewards for the given mission."""
        choice_ids = MISSION_CHOICES.get(mission_id, [])
        choices = []
        for tid in choice_ids:
            if tid in TECH_TREE:
                # Only offer choice if not already unlocked and not blocked
                # Actually, for mutual exclusion, we want to show it but maybe mark as unavailable?
                # Or just show valid options.
                # If I picked A, B is excluded. Should B still be offered? No, usually not.

                node = TECH_TREE[tid]
                is_blocked = any(conflict in self.unlocked_techs for conflict in node.mutually_exclusive_with)
                if tid not in self.unlocked_techs and not is_blocked:
                     choices.append(node)

        return choices

    def is_unit_unlocked(self, unit_name: str) -> bool:
        """Checks if a specific unit is unlocked.

        Args:
            unit_name: The name of the unit (e.g., 'rover').

        Returns:
            True if the unit is unlocked, False otherwise.
        """
        return unit_name in self.unlocked_units

    def get_tech_modifiers(self) -> List[Dict]:
        """Returns a list of all active modifiers from unlocked techs."""
        modifiers = []
        for tech_id in self.unlocked_techs:
            node = TECH_TREE.get(tech_id)
            if node:
                modifiers.extend(node.modifiers)
        return modifiers
