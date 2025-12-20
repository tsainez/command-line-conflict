from unittest.mock import Mock

from command_line_conflict.components.attack import Attack
from command_line_conflict.components.dead import Dead
from command_line_conflict.components.flee import Flee
from command_line_conflict.components.health import Health
from command_line_conflict.components.movable import Movable
from command_line_conflict.components.selectable import Selectable
from command_line_conflict.game_state import GameState
from command_line_conflict.systems.health_system import HealthSystem


def test_health_system_handles_death():
    # Arrange
    mock_map = Mock()
    game_state = GameState(game_map=mock_map)
    entity_id = game_state.create_entity()
    game_state.add_component(entity_id, Health(hp=0, max_hp=10, health_regen_rate=1))
    game_state.add_component(entity_id, Movable(speed=1.0))
    game_state.add_component(entity_id, Attack(attack_range=1, attack_damage=1, attack_speed=1))
    game_state.add_component(entity_id, Selectable())
    game_state.add_component(entity_id, Flee(flee_health_threshold=0.5))
    system = HealthSystem()

    # Act
    system.update(game_state, dt=1.0)

    # Assert
    assert game_state.get_component(entity_id, Dead) is not None
    assert game_state.get_component(entity_id, Movable) is None
    assert game_state.get_component(entity_id, Attack) is None
    assert game_state.get_component(entity_id, Selectable) is None
    assert game_state.get_component(entity_id, Flee) is None


def test_health_system_handles_regeneration():
    # Arrange
    mock_map = Mock()
    game_state = GameState(game_map=mock_map)
    entity_id = game_state.create_entity()
    health = Health(hp=5, max_hp=10, health_regen_rate=1)
    game_state.add_component(entity_id, health)
    system = HealthSystem()

    # Act
    system.update(game_state, dt=1.0)

    # Assert
    assert health.hp == 6


def test_health_system_handles_regeneration_cap():
    # Arrange
    mock_map = Mock()
    game_state = GameState(game_map=mock_map)
    entity_id = game_state.create_entity()
    health = Health(hp=9.5, max_hp=10, health_regen_rate=1)
    game_state.add_component(entity_id, health)
    system = HealthSystem()

    # Act
    system.update(game_state, dt=1.0)

    # Assert
    assert health.hp == 10
