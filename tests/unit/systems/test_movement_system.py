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


def test_intelligent_unit_avoids_clipping_when_target_set_directly(game_state, movement_system):
    # This simulates CombatSystem setting target directly, bypassing set_target()

    # Create an intelligent 'rover' unit
    unit1_id = create_rover(game_state, x=4, y=5, player_id=1)
    movable = game_state.get_component(unit1_id, Movable)

    # Add a wall at (5, 5)
    game_state.map.add_wall(5, 5)

    # Set target directly (as CombatSystem does) beyond the wall
    movable.target_x = 7.0
    movable.target_y = 5.0
    movable.path = []  # Ensure path is empty initially

    # Run update loop
    # If bug exists, unit moves straight into wall at (5,5).
    # If fixed, unit pathfinds around.

    hit_wall = False
    for _ in range(20):
        movement_system.update(game_state, dt=0.5)

        pos = game_state.get_component(unit1_id, Position)
        # Verify it never enters the wall
        if int(pos.x) == 5 and int(pos.y) == 5:
            hit_wall = True
            break

    assert not hit_wall, "Unit clipped into wall!"

    # Verify it successfully navigated around
    pos = game_state.get_component(unit1_id, Position)
    # It should have moved towards the target, likely reaching (6, 5) or similar
    assert pos.x > 5, "Unit failed to navigate past the wall"
