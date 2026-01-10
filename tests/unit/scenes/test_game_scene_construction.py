from unittest.mock import MagicMock, patch

import pygame

from command_line_conflict.components.player import Player
from command_line_conflict.components.position import Position
from command_line_conflict.components.selectable import Selectable
from command_line_conflict.components.unit_identity import UnitIdentity
from command_line_conflict.scenes.game import GameScene


class MockGame:
    def __init__(self):
        self.screen = MagicMock()
        self.font = MagicMock()
        self.music_manager = MagicMock()
        self.scene_manager = MagicMock()
        self.steam = MagicMock()


def test_handle_construction_uses_unit_identity():
    # Arrange
    game = MockGame()

    # We mock CampaignManager within the module where it is used
    with patch("command_line_conflict.scenes.game.CampaignManager") as MockCampaignManager:
        mock_campaign = MockCampaignManager.return_value
        # Allow everything to be built
        mock_campaign.is_unit_unlocked.return_value = True

        game_scene = GameScene(game)
        game_scene.campaign_manager = mock_campaign

        game_state = game_scene.game_state

        # Create chassis (should build)
        chassis_id = game_state.create_entity()
        game_state.add_component(chassis_id, Position(10, 10))
        game_state.add_component(chassis_id, Player(1, True))
        game_state.add_component(chassis_id, Selectable())
        game_state.entities[chassis_id][Selectable].is_selected = True
        game_state.add_component(chassis_id, UnitIdentity("chassis"))

        # Create rover (should NOT build, even if selected)
        rover_id = game_state.create_entity()
        game_state.add_component(rover_id, Position(20, 20))
        game_state.add_component(rover_id, Player(1, True))
        game_state.add_component(rover_id, Selectable())
        game_state.entities[rover_id][Selectable].is_selected = True
        game_state.add_component(rover_id, UnitIdentity("rover"))

        # Mock the factory creation function
        with patch("command_line_conflict.factories.create_rover_factory") as mock_create_factory:
            # Act
            # Simulate 'R' key press (Build Rover Factory)
            # handle_event calls _handle_construction when 'R' is pressed
            # We call _handle_construction directly to avoid event processing overhead if desired,
            # but testing handle_event is more integration-like.
            # However, handle_event also does other things. Let's call _handle_construction directly for unit testing logic.
            game_scene._handle_construction(pygame.K_r)  # pylint: disable=protected-access

            # Assert
            # Should be called once for the chassis
            assert mock_create_factory.call_count == 1
            args, _ = mock_create_factory.call_args
            # Verify coordinates match the chassis (10, 10) not rover (20, 20)
            assert args[1] == 10
            assert args[2] == 10

            # Verify chassis was removed (consumed)
            assert chassis_id not in game_state.entities
            # Verify rover was NOT removed
            assert rover_id in game_state.entities
