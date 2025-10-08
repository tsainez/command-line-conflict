"""
This module contains integration tests that test the game's systems.
"""
import pygame
from unittest.mock import Mock, patch

from command_line_conflict import config, factories
from command_line_conflict.components.attack import Attack
from command_line_conflict.components.builder import Builder
from command_line_conflict.components.factory import Factory
from command_line_conflict.components.gatherer import Gatherer
from command_line_conflict.components.health import Health
from command_line_conflict.components.movable import Movable
from command_line_conflict.components.player import Player
from command_line_conflict.components.position import Position
from command_line_conflict.components.renderable import Renderable
from command_line_conflict.systems.ai_system import AISystem
from command_line_conflict.systems.combat_system import CombatSystem
from command_line_conflict.systems.factory_system import FactorySystem
from command_line_conflict.systems.movement_system import MovementSystem
from command_line_conflict.systems.resource_system import ResourceSystem


def test_chassis_pathfinding_around_wall(game_state):
    """
    Tests that a chassis unit can find a path around a wall.
    """
    # Add a wall to the game map
    game_state.map.add_wall(5, 7)
    game_state.map.add_wall(6, 7)
    game_state.map.add_wall(7, 7)

    # Create a chassis unit and set its target
    chassis_id = factories.create_chassis(game_state, 1, 7, player_id=1)
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
    arachnotron_id = factories.create_arachnotron(game_state, 1, 7, player_id=1)
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
    attacker_id = factories.create_chassis(game_state, 1, 7, player_id=1)
    defender_id = factories.create_chassis(game_state, 2, 7, player_id=2)

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


def test_extractor_gathers_minerals_with_resource_system(game_state):
    """
    Tests that an extractor with a Gatherer component can gather minerals
    using the new ResourceSystem.
    """
    # Create an extractor and a mineral patch
    extractor_id = factories.create_extractor(game_state, 5, 5, player_id=1)
    minerals_id = factories.create_minerals(game_state, 10, 10)
    initial_minerals = game_state.resources[1]["minerals"]
    minerals_pos = game_state.get_component(minerals_id, Position)

    # Initialize systems
    movement_system = MovementSystem()
    resource_system = ResourceSystem()

    # Set the extractor's target to the minerals
    gatherer = game_state.get_component(extractor_id, Gatherer)
    gatherer.target_resource_id = minerals_id
    movement_system.set_target(
        game_state, extractor_id, minerals_pos.x, minerals_pos.y
    )

    # Run the systems for a few seconds to allow the unit to move and gather
    for _ in range(50):  # 5 seconds of game time
        movement_system.update(game_state, dt=0.1)
        resource_system.update(game_state, dt=0.1)

    # Check that the player's minerals have increased
    final_minerals = game_state.resources[1]["minerals"]
    assert final_minerals > initial_minerals


def test_ai_builds_and_produces(game_state):
    """Tests that the AI can build a factory and then produce a unit."""
    # Create an AI extractor
    factories.create_extractor(game_state, 42, 38, player_id=2, is_human=False)
    game_state.resources[2]["minerals"] = 200 # Give AI plenty of resources

    # Initialize AI and other relevant systems
    ai_system = AISystem()
    factory_system = FactorySystem()

    # Run AI system to make it decide to build
    ai_system.update(game_state)

    # Check that a factory was created by the AI
    factory_id = None
    for entity_id, components in game_state.entities.items():
        if components.get(Renderable, {}).icon == "F":
            factory_id = entity_id
            break
    assert factory_id is not None, "AI did not build a factory"

    # Run AI and factory systems to produce a unit
    for _ in range(60): # 6 seconds of game time
        ai_system.update(game_state)
        factory_system.update(game_state, dt=0.1)

    # Check that a new unit was created by the factory
    new_unit_found = False
    for entity_id, components in game_state.entities.items():
        player = components.get(Player)
        if player and player.player_id == 2 and components.get(Renderable, {}).icon == "C":
            new_unit_found = True
            break
    assert new_unit_found, "AI factory did not produce a unit"