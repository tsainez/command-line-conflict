# TODO: Add a description of each test scenario. 
from command_line_conflict.game_state import GameState
from command_line_conflict.maps.simple_map import SimpleMap
from command_line_conflict import factories
from command_line_conflict.systems.movement_system import MovementSystem
from command_line_conflict.systems.combat_system import CombatSystem
from command_line_conflict.components.position import Position
from command_line_conflict.components.movable import Movable
from command_line_conflict.components.attack import Attack
from command_line_conflict.components.health import Health
from command_line_conflict.components.vision import Vision

# TODO: Expand these tests to cover more integration scenarios.
def test_chassis_pathfinding_around_wall():
    game_map = SimpleMap()
    game_map.add_wall(5, 7)
    game_map.add_wall(6, 7)
    game_map.add_wall(7, 7)
    game_state = GameState(game_map)
    movement_system = MovementSystem()
    chassis_id = factories.create_chassis(game_state, 1, 7)
    chassis_movable = game_state.get_component(chassis_id, Movable)
    chassis_movable.target_x = 18
    chassis_movable.target_y = 7
    chassis_movable.path = game_map.find_path((1, 7), (18, 7))
    assert chassis_movable.path is not None
    assert len(chassis_movable.path) > 1
    # The path should go around the wall, so it must contain y-coordinates other than 7
    assert any(y != 7 for x, y in chassis_movable.path)


def test_arachnotron_pathfinding_over_wall():
    game_map = SimpleMap()
    game_map.add_wall(5, 7)
    game_map.add_wall(6, 7)
    game_map.add_wall(7, 7)
    game_state = GameState(game_map)
    movement_system = MovementSystem()
    arachnotron_id = factories.create_arachnotron(game_state, 1, 7)
    arachnotron_movable = game_state.get_component(arachnotron_id, Movable)
    arachnotron_movable.target_x = 18
    arachnotron_movable.target_y = 7
    arachnotron_movable.path = game_map.find_path(
        (1, 7), (18, 7), can_fly=True
    )
    assert arachnotron_movable.path is not None
    assert len(arachnotron_movable.path) > 1
    # The path should go over the wall, so it must contain y-coordinates of 7
    assert all(y == 7 for x, y in arachnotron_movable.path)


def test_combat_system():
    game_map = SimpleMap()
    game_state = GameState(game_map)
    combat_system = CombatSystem()
    attacker_id = factories.create_chassis(game_state, 1, 7)
    defender_id = factories.create_chassis(game_state, 2, 7)
    attacker_attack = game_state.get_component(attacker_id, Attack)
    defender_health = game_state.get_component(defender_id, Health)
    initial_hp = defender_health.hp
    attacker_attack.attack_target = defender_id
    combat_system.update(game_state, 0.1)
    assert defender_health.hp < initial_hp
