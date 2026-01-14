import os
from unittest.mock import MagicMock
import pygame

# Set headless
os.environ["SDL_VIDEODRIVER"] = "dummy"

from command_line_conflict.scenes.game import GameScene
from command_line_conflict.components.player import Player
from command_line_conflict.components.health import Health
from command_line_conflict.components.position import Position
from command_line_conflict import config

def test_check_win_condition():
    # Setup
    mock_game = MagicMock()
    mock_game.screen = pygame.display.get_surface()
    mock_game.font = pygame.font.Font(None, 24)
    mock_game.music_manager = MagicMock()
    mock_game.steam = MagicMock()
    scene = GameScene(mock_game)

    # Mock campaign manager to prevent side effects (file I/O)
    scene.campaign_manager = MagicMock()

    scene.game_state.entities.clear()
    scene.game_state.component_index.clear()
    scene.game_state.spatial_map.clear()

    # 1. Start with no enemies -> Win
    assert scene.check_win_condition() is True

    # 2. Add Enemy -> No Win
    enemy_id = scene.game_state.create_entity()
    scene.game_state.add_component(enemy_id, Player(2, is_human=False))
    scene.game_state.add_component(enemy_id, Health(100, 100))
    scene.game_state.add_component(enemy_id, Position(10, 10))

    assert scene.check_win_condition() is False

    # 3. Remove Health component manually (simulating death logic that removes it or entity)
    scene.game_state.remove_component(enemy_id, Health)
    assert scene.check_win_condition() is True

def test_check_loss_condition():
    # Setup
    mock_game = MagicMock()
    mock_game.screen = pygame.display.get_surface()
    mock_game.font = pygame.font.Font(None, 24)
    mock_game.music_manager = MagicMock()
    mock_game.steam = MagicMock()
    scene = GameScene(mock_game)

    # Mock campaign manager
    scene.campaign_manager = MagicMock()

    scene.game_state.entities.clear()
    scene.game_state.component_index.clear()
    scene.game_state.spatial_map.clear()

    # 1. No player units -> Loss
    assert scene.check_loss_condition() is True

    # 2. Add Player Unit -> No Loss
    player_id = scene.game_state.create_entity()
    scene.game_state.add_component(player_id, Player(1, is_human=True))
    scene.game_state.add_component(player_id, Health(100, 100))

    assert scene.check_loss_condition() is False

    # 3. Add Dummy Entity (no Player component) -> Still No Loss (because player unit exists)
    dummy_id = scene.game_state.create_entity()
    scene.game_state.add_component(dummy_id, Position(0, 0))

    assert scene.check_loss_condition() is False

    # 4. Remove Player Unit -> Loss
    scene.game_state.remove_entity(player_id)
    assert scene.check_loss_condition() is True
