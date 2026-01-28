from unittest.mock import MagicMock

import pygame
import pytest

from command_line_conflict import config
from command_line_conflict.components.attack import Attack
from command_line_conflict.components.health import Health
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
        # Mock screen get_size for grid drawing logic
        self.screen.get_size.return_value = (800, 600)
        self.running = True


def test_right_click_enemy_issues_attack_command(mocker):
    """
    Verifies that right-clicking an enemy unit issues an ATTACK command
    instead of a MOVE command for selected units.
    """
    # Arrange
    mocker.patch("command_line_conflict.config.DEBUG", True)

    # Mock camera to ensure screen_to_grid returns predictable values
    # We'll rely on the default Camera behavior but ensure zoom/pos are default

    game = MockGame()
    scene = GameScene(game)
    game_state = scene.game_state

    # 1. Create Player 1 Unit (Attacker)
    attacker_id = game_state.create_entity()
    game_state.add_component(attacker_id, Position(10, 10))
    game_state.add_component(attacker_id, Player(player_id=1, is_human=True))
    selectable = Selectable()
    selectable.is_selected = True
    game_state.add_component(attacker_id, selectable)
    game_state.add_component(attacker_id, Attack(attack_damage=10, attack_range=5, attack_speed=1.0))
    # Add Movable so we can check if it tries to move
    from command_line_conflict.components.movable import Movable
    game_state.add_component(attacker_id, Movable(speed=5.0))

    # 2. Create Player 2 Unit (Target) at (12, 12)
    target_id = game_state.create_entity()
    game_state.add_component(target_id, Position(12, 12))
    game_state.add_component(target_id, Player(player_id=2, is_human=False))
    game_state.add_component(target_id, Health(hp=100, max_hp=100))
    # We need to make sure the game state knows this entity is at (12, 12) in the spatial map
    # GameState.add_component doesn't automatically update spatial map unless we call update_entity_position
    # But create_entity just makes ID.
    # Let's manually ensure spatial map is correct or use update_entity_position
    game_state.update_entity_position(target_id, 12.0, 12.0)

    # 3. Simulate Right-Click on Target's position
    # We need to calculate screen coordinates for grid (12, 12)
    # Default camera x=0, y=0, zoom=1.0, GRID_SIZE=32 (usually)
    grid_size = config.GRID_SIZE
    screen_x = 12 * grid_size + grid_size // 2
    screen_y = 12 * grid_size + grid_size // 2

    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 3, "pos": (screen_x, screen_y)})

    # Act
    scene.handle_event(event)

    # Assert
    attacker_attack = game_state.get_component(attacker_id, Attack)
    attacker_movable = game_state.get_component(attacker_id, Movable)

    # Expectation: Attack target should be set to target_id
    assert attacker_attack.attack_target == target_id, "Right-click on enemy should set attack target"

    # Expectation: Should NOT set a move target to the enemy's location (optional, depends on implementation preference)
    # Ideally for "Attack Move", we might move towards it in CombatSystem, but handle_event shouldn't blindly set move target.
    # If handle_event sets move target, CombatSystem might override it, but it's cleaner if it doesn't.
    # However, existing logic clears attack_target if moving.

    # Verify visual feedback (Red ripple)
    # We need to check scene.ui_system.click_effects
    # The last effect should be red (255, 0, 0)
    assert len(scene.ui_system.click_effects) > 0
    last_effect = scene.ui_system.click_effects[-1]
    assert last_effect["color"] == (255, 0, 0), "Should show red ripple for attack command"
    assert last_effect["x"] == 12
    assert last_effect["y"] == 12

def test_right_click_ground_issues_move_command(mocker):
    """
    Verifies that right-clicking empty ground issues a MOVE command
    and clears attack target.
    """
    # Arrange
    mocker.patch("command_line_conflict.config.DEBUG", True)

    game = MockGame()
    scene = GameScene(game)
    game_state = scene.game_state

    # 1. Create Player 1 Unit
    attacker_id = game_state.create_entity()
    game_state.add_component(attacker_id, Position(10, 10))
    game_state.add_component(attacker_id, Player(player_id=1, is_human=True))
    selectable = Selectable()
    selectable.is_selected = True
    game_state.add_component(attacker_id, selectable)
    game_state.add_component(attacker_id, Attack(attack_damage=10, attack_range=5, attack_speed=1.0))
    from command_line_conflict.components.movable import Movable
    game_state.add_component(attacker_id, Movable(speed=5.0))

    # Set an existing attack target
    dummy_target = game_state.create_entity()
    game_state.get_component(attacker_id, Attack).attack_target = dummy_target

    # 3. Simulate Right-Click on Empty Ground (15, 15)
    grid_size = config.GRID_SIZE
    screen_x = 15 * grid_size + grid_size // 2
    screen_y = 15 * grid_size + grid_size // 2

    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 3, "pos": (screen_x, screen_y)})

    # Act
    scene.handle_event(event)

    # Assert
    attacker_attack = game_state.get_component(attacker_id, Attack)
    attacker_movable = game_state.get_component(attacker_id, Movable)

    # Expectation: Attack target should be CLEARED
    assert attacker_attack.attack_target is None, "Right-click on ground should clear attack target"

    # Expectation: Move target should be set
    assert attacker_movable.target_x == 15
    assert attacker_movable.target_y == 15

    # Verify visual feedback (Green ripple)
    assert len(scene.ui_system.click_effects) > 0
    last_effect = scene.ui_system.click_effects[-1]
    assert last_effect["color"] == (0, 255, 0), "Should show green ripple for move command"
