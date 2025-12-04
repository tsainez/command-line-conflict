
import pytest
from command_line_conflict.components.attack import Attack
from command_line_conflict.components.player import Player
from command_line_conflict.components.position import Position
from command_line_conflict.components.vision import Vision
from command_line_conflict.systems.ai_system import AISystem


def test_ai_system_acquires_target(game_state):
    """
    Test that the AI system correctly acquires a target for a unit with attack capability
    when an enemy is within vision range.
    """
    ai_system = AISystem()

    # Create AI unit (Player 2)
    ai_unit = game_state.create_entity()
    game_state.add_component(ai_unit, Player(player_id=2))
    game_state.add_component(ai_unit, Position(x=10, y=10))
    game_state.add_component(ai_unit, Vision(vision_range=5))
    game_state.add_component(ai_unit, Attack(attack_damage=10, attack_range=2, attack_speed=1.0))

    # Create Enemy unit (Player 1)
    enemy_unit = game_state.create_entity()
    game_state.add_component(enemy_unit, Player(player_id=1))
    game_state.add_component(enemy_unit, Position(x=12, y=10)) # Within vision range

    # Run AI System
    ai_system.update(game_state)

    # Check if target acquired
    attack_comp = game_state.get_component(ai_unit, Attack)
    assert attack_comp.attack_target == enemy_unit

def test_ai_system_ignores_distant_enemy(game_state):
    """
    Test that the AI system does not acquire a target if the enemy is outside vision range.
    """
    ai_system = AISystem()

    # Create AI unit (Player 2)
    ai_unit = game_state.create_entity()
    game_state.add_component(ai_unit, Player(player_id=2))
    game_state.add_component(ai_unit, Position(x=10, y=10))
    game_state.add_component(ai_unit, Vision(vision_range=5))
    game_state.add_component(ai_unit, Attack(attack_damage=10, attack_range=2, attack_speed=1.0))

    # Create Enemy unit (Player 1)
    enemy_unit = game_state.create_entity()
    game_state.add_component(enemy_unit, Player(player_id=1))
    game_state.add_component(enemy_unit, Position(x=20, y=10)) # Outside vision range

    # Run AI System
    ai_system.update(game_state)

    # Check that no target is acquired
    attack_comp = game_state.get_component(ai_unit, Attack)
    assert attack_comp.attack_target is None

def test_ai_system_ignores_friendly(game_state):
    """
    Test that the AI system does not target friendly units.
    """
    ai_system = AISystem()

    # Create AI unit (Player 2)
    ai_unit = game_state.create_entity()
    game_state.add_component(ai_unit, Player(player_id=2))
    game_state.add_component(ai_unit, Position(x=10, y=10))
    game_state.add_component(ai_unit, Vision(vision_range=5))
    game_state.add_component(ai_unit, Attack(attack_damage=10, attack_range=2, attack_speed=1.0))

    # Create Friendly unit (Player 2)
    friendly_unit = game_state.create_entity()
    game_state.add_component(friendly_unit, Player(player_id=2))
    game_state.add_component(friendly_unit, Position(x=11, y=10))

    # Run AI System
    ai_system.update(game_state)

    # Check that no target is acquired
    attack_comp = game_state.get_component(ai_unit, Attack)
    assert attack_comp.attack_target is None
