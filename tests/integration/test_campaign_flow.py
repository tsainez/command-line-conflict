import json
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from command_line_conflict.campaign_manager import CampaignManager


class TestCampaignFlow:
    @pytest.fixture
    def temp_data_dir(self):
        with tempfile.TemporaryDirectory() as tmpdirname:
            yield Path(tmpdirname)

    def test_new_campaign_starts_fresh(self, temp_data_dir):
        """Test that a new campaign starts with no completed missions and default unlocks."""
        with patch("command_line_conflict.campaign_manager.get_user_data_dir", return_value=temp_data_dir):
            manager = CampaignManager()

            assert manager.completed_missions == []
            assert manager.unlocked_units == {"chassis", "extractor"}
            assert not (temp_data_dir / "save_game.json").exists()

    def test_complete_mission_saves_progress_and_unlocks_units(self, temp_data_dir):
        """Test that completing a mission saves progress and unlocks the reward."""
        with patch("command_line_conflict.campaign_manager.get_user_data_dir", return_value=temp_data_dir):
            manager = CampaignManager()

            # Complete Mission 1
            manager.complete_mission("mission_1")

            # Verify internal state
            assert "mission_1" in manager.completed_missions
            assert "rover" in manager.unlocked_units

            # Verify file persistence
            save_file = temp_data_dir / "save_game.json"
            assert save_file.exists()

            with open(save_file, "r") as f:
                data = json.load(f)
                assert "mission_1" in data["completed_missions"]

    def test_load_existing_campaign(self, temp_data_dir):
        """Test that a new manager instance loads progress from an existing save file."""
        # Create a fake save file
        save_file = temp_data_dir / "save_game.json"
        data = {"completed_missions": ["mission_1", "mission_2"]}
        with open(save_file, "w") as f:
            json.dump(data, f)

        with patch("command_line_conflict.campaign_manager.get_user_data_dir", return_value=temp_data_dir):
            manager = CampaignManager()

            # Verify loaded state
            assert "mission_1" in manager.completed_missions
            assert "mission_2" in manager.completed_missions

            # Verify rewards from both missions are unlocked
            assert "rover" in manager.unlocked_units  # From mission 1
            assert "arachnotron" in manager.unlocked_units  # From mission 2

    def test_campaign_progression_flow(self, temp_data_dir):
        """Simulate a full campaign progression."""
        with patch("command_line_conflict.campaign_manager.get_user_data_dir", return_value=temp_data_dir):
            manager = CampaignManager()

            # Start
            assert "rover" not in manager.unlocked_units

            # Win Mission 1
            manager.complete_mission("mission_1")
            assert "rover" in manager.unlocked_units
            assert "arachnotron" not in manager.unlocked_units

            # Win Mission 2
            manager.complete_mission("mission_2")
            assert "arachnotron" in manager.unlocked_units

            # Reload to ensure persistence
            new_manager = CampaignManager()
            assert "mission_1" in new_manager.completed_missions
            assert "mission_2" in new_manager.completed_missions
            assert "arachnotron" in new_manager.unlocked_units
