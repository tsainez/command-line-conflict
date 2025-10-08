import pygame
import pytest
from unittest.mock import Mock

from command_line_conflict import factories
from command_line_conflict.components.building import Building
from command_line_conflict.components.gatherer import Gatherer
from command_line_conflict.components.player import Player
from command_line_conflict.components.position import Position
from command_line_conflict.components.selectable import Selectable
from command_line_conflict.scenes.game import GameScene


class MockGame:
    def __init__(self):
        self.screen = None
        self.font = None
        self.scene_manager = None


@pytest.fixture
def game_scene():
    """Fixture to create a GameScene with mocked dependencies."""
    # Prevent pygame from trying to initialize video/font
    pygame.display.init = lambda: None
    pygame.font.init = lambda: None
    game = MockGame()
    scene = GameScene(game)
    # Clear default units for clean test slate
    scene.game_state.entities = {}
    return scene


def test_win_condition(game_scene):
    """Tests that the game correctly identifies a winner when all buildings are destroyed."""
    # Initially, no one has had buildings
    assert not game_scene.player1_had_building
    assert not game_scene.player2_had_building
    assert not game_scene.game_over

    # Player 1 builds a building
    player1_building = game_scene.game_state.create_entity()
    game_scene.game_state.add_component(player1_building, Building())
    game_scene.game_state.add_component(player1_building, Player(player_id=1))
    game_scene.game_state.add_component(player1_building, Position(1, 1))

    # Player 2 builds a building
    player2_building = game_scene.game_state.create_entity()
    game_scene.game_state.add_component(player2_building, Building())
    game_scene.game_state.add_component(player2_building, Player(player_id=2))
    game_scene.game_state.add_component(player2_building, Position(2, 2))

    # Game should not be over yet, but flags should be set
    game_scene._check_win_condition()
    assert not game_scene.game_over
    assert game_scene.player1_had_building
    assert game_scene.player2_had_building

    # Player 1 loses their building
    game_scene.game_state.remove_entity(player1_building)

    # Game should be over, player 2 wins
    game_scene._check_win_condition()
    assert game_scene.game_over
    assert game_scene.winner == 2


def test_player_can_gather_minerals(game_scene):
    """Tests that a player can right-click minerals to gather them and that resources increase."""
    # Create an extractor and select it
    extractor_id = factories.create_extractor(
        game_scene.game_state, 14, 15, 1, is_human=True
    )
    game_scene.game_state.get_component(extractor_id, Selectable).is_selected = True
    initial_resources = game_scene.game_state.resources[1]["minerals"]

    # Create a mineral patch
    minerals_id = factories.create_minerals(game_scene.game_state, 15, 15)

    # Simulate a right-click on the minerals
    game_scene.camera = Mock()
    game_scene.camera.screen_to_grid.return_value = (15, 15)
    event = Mock()
    event.type = pygame.MOUSEBUTTONDOWN
    event.button = 3
    event.pos = (200, 200)  # Position doesn't matter as screen_to_grid is mocked
    game_scene.handle_event(event)

    # Check that the extractor is targeting the minerals
    gatherer = game_scene.game_state.get_component(extractor_id, Gatherer)
    assert gatherer.target_resource_id == minerals_id

    # Let the systems run for a bit to simulate gathering
    for _ in range(10): # 1 second of game time
        game_scene.movement_system.update(game_scene.game_state, dt=0.1)
        game_scene.resource_system.update(game_scene.game_state, dt=0.1)

    # Check that the player's resources have increased
    final_resources = game_scene.game_state.resources[1]["minerals"]
    assert final_resources > initial_resources