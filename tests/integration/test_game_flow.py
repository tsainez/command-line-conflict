"""
This module contains integration tests that test the game's systems.
"""

from command_line_conflict import factories
from command_line_conflict.components.attack import Attack
from command_line_conflict.components.health import Health
from command_line_conflict.components.movable import Movable
from command_line_conflict.systems.combat_system import CombatSystem
from command_line_conflict.systems.movement_system import MovementSystem


def test_chassis_pathfinding_around_wall(game_state):
    """
    Tests that a chassis unit can find a path around a wall.
    """
    # Add a wall to the game map
    game_state.map.add_wall(5, 7)
    game_state.map.add_wall(6, 7)
    game_state.map.add_wall(7, 7)

    # Create a chassis unit and set its target
    chassis_id = factories.create_chassis(game_state, 1, 7, 1)
    chassis_movable = game_state.get_component(chassis_id, Movable)
    chassis_movable.target_x = 18
    chassis_movable.target_y = 7

    # Find a path to the target
    chassis_movable.path = game_state.map.find_path((1, 7), (18, 7))

    # Check that the path is valid and goes around the wall
    assert chassis_movable.path is not None
    assert len(chassis_movable.path) > 1
    assert any(y != 7 for x, y in chassis_movable.path)


def test_arachnotron_pathfinding_over_wall(game_state):
    """
    Tests that an arachnotron unit can find a path over a wall.
    """
    # Add a wall to the game map
    game_state.map.add_wall(5, 7)
    game_state.map.add_wall(6, 7)
    game_state.map.add_wall(7, 7)

    # Create an arachnotron unit and set its target
    arachnotron_id = factories.create_arachnotron(game_state, 1, 7, 1)
    arachnotron_movable = game_state.get_component(arachnotron_id, Movable)
    arachnotron_movable.target_x = 18
    arachnotron_movable.target_y = 7

    # Find a path to the target
    arachnotron_movable.path = game_state.map.find_path((1, 7), (18, 7), can_fly=True)

    # Check that the path is valid and goes over the wall
    assert arachnotron_movable.path is not None
    assert len(arachnotron_movable.path) > 1
    assert all(y == 7 for x, y in arachnotron_movable.path)


def test_unit_takes_damage_in_combat(game_state):
    """
    Tests that a unit takes damage when it is attacked.
    """
    # Create an attacker and a defender
    attacker_id = factories.create_chassis(game_state, 1, 7, 1)
    defender_id = factories.create_chassis(game_state, 2, 7, 2)

    # Get the defender's health
    defender_health = game_state.get_component(defender_id, Health)
    initial_hp = defender_health.hp

    # Set the attacker's target to the defender
    attacker_attack = game_state.get_component(attacker_id, Attack)
    attacker_attack.attack_target = defender_id

    # Update the combat system
    combat_system = CombatSystem()
    combat_system.update(game_state, 0.1)

    # Check that the defender has taken damage
    assert defender_health.hp < initial_hp
