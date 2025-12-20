from unittest.mock import MagicMock

import pygame

from command_line_conflict.components.attack import Attack
from command_line_conflict.components.position import Position
from command_line_conflict.components.selectable import Selectable
from command_line_conflict.scenes.game import GameScene


class MockGame:
    def __init__(self):
        self.screen = None
        self.font = None
        self.music_manager = MagicMock()


def test_move_command_interrupts_attack():
    # Arrange
    game = MockGame()
    game_scene = GameScene(game)
    game_state = game_scene.game_state

    attacker_id = game_state.create_entity()
    game_state.add_component(attacker_id, Position(0, 0))
    game_state.add_component(attacker_id, Attack(attack_damage=10, attack_range=5, attack_speed=1.0))
    game_state.add_component(attacker_id, Selectable())
    game_state.entities[attacker_id][Selectable].is_selected = True

    target_id = game_state.create_entity()
    game_state.add_component(target_id, Position(3, 3))
    game_state.entities[attacker_id][Attack].attack_target = target_id

    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 3, "pos": (100, 100)})

    # Act
    game_scene.handle_event(event)

    # Assert
    assert game_state.entities[attacker_id][Attack].attack_target is None
