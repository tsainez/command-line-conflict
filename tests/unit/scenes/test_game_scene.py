import pygame

from command_line_conflict.scenes.game import GameScene
from command_line_conflict.components.building import Building
from command_line_conflict.components.player import Player
from command_line_conflict.components.position import Position


class MockGame:
    def __init__(self):
        self.screen = None
        self.font = None
        self.scene_manager = None


def test_win_condition():
    """Tests that the game correctly identifies a winner when all buildings are destroyed."""
    # Prevent pygame from trying to initialize video
    pygame.display.init = lambda: None
    pygame.font.init = lambda: None

    game = MockGame()
    game_scene = GameScene(game)

    # Initially, no one has buildings
    assert not game_scene.player1_has_buildings
    assert not game_scene.player2_has_buildings
    assert not game_scene.game_over

    # Player 1 builds a building
    player1_building = game_scene.game_state.create_entity()
    game_scene.game_state.add_component(player1_building, Building())
    game_scene.game_state.add_component(player1_building, Player(player_id=1))
    game_scene.game_state.add_component(player1_building, Position(1, 1))
    game_scene.player1_has_buildings = True

    # Player 2 builds a building
    player2_building = game_scene.game_state.create_entity()
    game_scene.game_state.add_component(player2_building, Building())
    game_scene.game_state.add_component(player2_building, Player(player_id=2))
    game_scene.game_state.add_component(player2_building, Position(2, 2))
    game_scene.player2_has_buildings = True

    # Game should not be over
    game_scene._check_win_condition()
    assert not game_scene.game_over

    # Player 1 loses their building
    game_scene.game_state.remove_entity(player1_building)

    # Game should be over, player 2 wins
    game_scene._check_win_condition()
    assert game_scene.game_over
    assert game_scene.winner == 2