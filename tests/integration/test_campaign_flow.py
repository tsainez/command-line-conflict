import os
import pytest
import pygame
from unittest.mock import MagicMock, patch

from command_line_conflict.campaign_manager import CampaignManager, MISSIONS
from command_line_conflict.scenes.tech_database import TechDatabaseScene
from command_line_conflict.scenes.mission_select import MissionSelectScene
from command_line_conflict.scenes.briefing import BriefingScene
from command_line_conflict.scenes.game import GameScene
from command_line_conflict.game_state import GameState
from command_line_conflict.components.player import Player

# Mock Game Class
class MockGame:
    def __init__(self):
        self.font = MagicMock()
        self.scene_manager = MagicMock()
        self.screen = MagicMock()
        self.music_manager = MagicMock()
        self.running = True
        self.current_mission_id = "mission_1"

@pytest.fixture
def mock_game():
    return MockGame()

@pytest.fixture
def mock_campaign_manager():
    cm = CampaignManager()
    # Reset for tests
    cm.completed_missions = []
    cm.unlocked_units = {"chassis", "extractor"}
    return cm

class TestCampaignFlow:

    def test_tech_database_initialization(self, mock_game):
        """Test that Tech Database loads unlocked units."""
        with patch('command_line_conflict.scenes.tech_database.CampaignManager') as mock_cm_cls:
            mock_cm = mock_cm_cls.return_value
            mock_cm.unlocked_units = {"chassis", "rover"}

            scene = TechDatabaseScene(mock_game)

            assert "chassis" in scene.units
            assert "rover" in scene.units
            assert len(scene.unit_stats) > 0

    def test_mission_select_navigation(self, mock_game):
        """Test Mission Select logic."""
        with patch('command_line_conflict.scenes.mission_select.CampaignManager') as mock_cm_cls:
            mock_cm = mock_cm_cls.return_value
            mock_cm.get_all_missions.return_value = MISSIONS
            mock_cm.is_mission_unlocked.side_effect = lambda mid: mid == "mission_1"

            scene = MissionSelectScene(mock_game)

            # Select first mission (unlocked)
            scene.selected_index = 0
            event = MagicMock(type=pygame.KEYDOWN, key=pygame.K_RETURN)
            scene.handle_event(event)

            assert mock_game.current_mission_id == "mission_1"
            mock_game.scene_manager.switch_to.assert_called_with("briefing")

            # Select second mission (locked)
            mock_game.scene_manager.reset_mock()
            scene.selected_index = 1
            scene.handle_event(event)

            # Should not switch
            mock_game.scene_manager.switch_to.assert_not_called()

    def test_briefing_scene(self, mock_game):
        """Test Briefing Scene displays correct text."""
        mock_game.current_mission_id = "mission_1"
        scene = BriefingScene(mock_game)

        assert scene.mission_data["id"] == "mission_1"
        assert "First Contact" in scene.mission_data["title"]

        # Test transition
        event = MagicMock(type=pygame.KEYDOWN, key=pygame.K_RETURN)
        scene.handle_event(event)
        mock_game.scene_manager.switch_to.assert_called_with("game")

    @patch('command_line_conflict.scenes.game.factories')
    def test_game_scene_mission_loading(self, mock_factories, mock_game):
        """Test GameScene loads units based on mission."""
        mock_game.current_mission_id = "mission_2"

        # Mock GameState to avoid actual game logic
        with patch('command_line_conflict.scenes.game.GameState') as mock_state_cls:
            with patch('command_line_conflict.scenes.game.FogOfWar'), \
                 patch('command_line_conflict.scenes.game.RenderingSystem'), \
                 patch('command_line_conflict.scenes.game.UISystem'), \
                 patch('command_line_conflict.scenes.game.ChatSystem'), \
                 patch('command_line_conflict.scenes.game.SoundSystem'):

                # Mock game state entities to avoid validation errors
                mock_gs = mock_state_cls.return_value
                mock_gs.entities = {}

                scene = GameScene(mock_game)

                # Verify Mission 2 specific units were called
                assert mock_factories.create_arachnotron.called
                assert mock_factories.create_rover.called
