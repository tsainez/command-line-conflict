import pytest

from command_line_conflict.components.position import Position
from command_line_conflict.factories import create_observer, create_rover
from command_line_conflict.game_state import GameState
from command_line_conflict.maps.base import Map
from command_line_conflict.systems.flee_system import FleeSystem
from command_line_conflict.systems.movement_system import MovementSystem


@pytest.fixture
def game_state():
    game_map = Map(width=20, height=20)
    return GameState(game_map=game_map)


def test_observer_flees_when_detected(game_state):
    # Create an observer and an enemy
    observer_id = create_observer(game_state=game_state, x=10, y=10, player_id=1)
    enemy_id = create_rover(game_state=game_state, x=10, y=11, player_id=2)

    # Get the initial position of the observer
    initial_position = game_state.get_component(observer_id, Position)
    initial_x, initial_y = initial_position.x, initial_position.y

    # Create and run the systems
    flee_system = FleeSystem()
    movement_system = MovementSystem()
    flee_system.update(game_state, 1.0)
    movement_system.update(game_state, 1.0)

    # Get the new position of the observer
    new_position = game_state.get_component(observer_id, Position)
    new_x, new_y = new_position.x, new_position.y

    # Check that the observer has moved
    assert (initial_x, initial_y) != (new_x, new_y)
