import pytest

from command_line_conflict.components.movable import Movable
from command_line_conflict.components.position import Position
from command_line_conflict.factories import create_chassis, create_rover
from command_line_conflict.game_state import GameState
from command_line_conflict.maps.simple_map import SimpleMap
from command_line_conflict.systems.movement_system import MovementSystem


@pytest.fixture
def game_state():
    return GameState(SimpleMap())


@pytest.fixture
def movement_system():
    return MovementSystem()


def test_non_intelligent_unit_stops_at_obstacle(game_state, movement_system):
    # Create a non-intelligent 'chassis' unit
    unit1_id = create_chassis(game_state, x=10, y=10, player_id=1)
    # Create a second unit to act as an obstacle
    create_chassis(game_state, x=10, y=11, player_id=2)

    # Try to move unit1 into the space occupied by unit2
    movement_system.set_target(game_state, unit1_id, 10, 11)

    # Let the system update a few times
    for _ in range(5):
        movement_system.update(game_state, dt=0.1)

    unit1_pos = game_state.get_component(unit1_id, Position)

    # The unit should not have moved into the occupied space.
    # It might have moved slightly towards it, but not onto the square.
    assert int(unit1_pos.x) == 10 and int(unit1_pos.y) == 10


def test_intelligent_unit_moves_around_obstacle(game_state, movement_system):
    # Create an intelligent 'rover' unit
    unit1_id = create_rover(game_state, x=10, y=10, player_id=1)
    unit1_movable = game_state.get_component(unit1_id, Movable)
    assert unit1_movable.intelligent is True

    # Create a second unit to act as an obstacle
    create_chassis(game_state, x=10, y=11, player_id=2)

    # Set a target on the other side of the obstacle
    movement_system.set_target(game_state, unit1_id, 10, 12)

    unit1_movable = game_state.get_component(unit1_id, Movable)

    # The path should not be empty, and it should not go through the obstacle
    assert len(unit1_movable.path) > 0
    assert (10, 11) not in unit1_movable.path

    # Let the system update enough times for the unit to move
    for _ in range(20):
        movement_system.update(game_state, dt=0.1)

    unit1_pos = game_state.get_component(unit1_id, Position)

    # The unit should have moved to the target
    assert int(unit1_pos.x) == 10 and int(unit1_pos.y) == 12


def test_units_do_not_overlap(game_state, movement_system):
    """Tests that two units do not move into the same space."""
    # Create two intelligent 'rover' units
    unit1_id = create_rover(game_state, x=10, y=10, player_id=1)
    unit2_id = create_rover(game_state, x=12, y=10, player_id=2)

    # Set the same target for both units
    target_x, target_y = 11, 10
    movement_system.set_target(game_state, unit1_id, target_x, target_y)
    movement_system.set_target(game_state, unit2_id, target_x, target_y)

    # Let the system update enough times for the units to move
    for _ in range(10):
        movement_system.update(game_state, dt=0.1)

    unit1_pos = game_state.get_component(unit1_id, Position)
    unit2_pos = game_state.get_component(unit2_id, Position)

    # Check that the two units are not in the same grid cell
    assert (int(unit1_pos.x), int(unit1_pos.y)) != (
        int(unit2_pos.x),
        int(unit2_pos.y),
    )

    # Check that one of them made it to the target
    unit1_at_target = (int(unit1_pos.x), int(unit1_pos.y)) == (target_x, target_y)
    unit2_at_target = (int(unit2_pos.x), int(unit2_pos.y)) == (target_x, target_y)
    assert unit1_at_target or unit2_at_target
