# pylint: disable=redefined-outer-name
"""Tests for the basic worker (chassis) stuck-ping micro behavior.

The chassis is non-intelligent by design: it does NOT use pathfinding and
should walk in a straight line. When it bumps into an obstacle (a wall or
another unit), the movement system pings the player via a chat-log event.
"""

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


def _drain_log_events(game_state: GameState):
    return [e for e in game_state.event_queue if e.get("type") == "log"]


def test_chassis_does_not_pathfind_around_wall(game_state, movement_system):
    """A chassis must not produce an A* path; it should walk straight."""
    unit_id = create_chassis(game_state, x=2, y=5, player_id=1, is_human=True)

    # Place a wall directly between the chassis and its destination.
    game_state.map.add_wall(5, 5)

    movement_system.set_target(game_state, unit_id, 9, 5)

    movable = game_state.get_component(unit_id, Movable)
    assert movable.path == [], "Chassis must not pathfind"
    assert movable.target_x == 9 and movable.target_y == 5


def test_rover_still_pathfinds(game_state, movement_system):
    """A rover (intelligent) keeps pathfinding for comparison."""
    unit_id = create_rover(game_state, x=2, y=5, player_id=1, is_human=True)
    game_state.map.add_wall(5, 5)

    movement_system.set_target(game_state, unit_id, 9, 5)

    movable = game_state.get_component(unit_id, Movable)
    assert movable.path, "Rover must produce an A* path around the wall"
    assert (5, 5) not in movable.path


def test_chassis_pings_player_when_blocked_by_wall(game_state, movement_system):
    """When the chassis runs into a wall it must emit a stuck log event."""
    unit_id = create_chassis(game_state, x=2, y=5, player_id=1, is_human=True)
    game_state.map.add_wall(5, 5)

    movement_system.set_target(game_state, unit_id, 9, 5)

    # Walk forward until the chassis hits the wall (chassis speed 2, dt 0.1).
    for _ in range(40):
        movement_system.update(game_state, dt=0.1)

    log_events = _drain_log_events(game_state)
    assert log_events, "Expected a stuck-ping log event for the chassis"
    assert any("terrain" in e["text"].lower() or "stuck" in e["text"].lower() for e in log_events)

    # The order is cleared so the unit doesn't keep grinding into the wall.
    movable = game_state.get_component(unit_id, Movable)
    assert movable.target_x is None and movable.target_y is None

    # Position should not have entered the wall tile.
    pos = game_state.get_component(unit_id, Position)
    assert int(pos.x) < 5


def test_chassis_pings_player_when_blocked_by_unit(game_state, movement_system):
    """When another unit blocks the path, ping the player exactly once."""
    unit_id = create_chassis(game_state, x=10, y=10, player_id=1, is_human=True)
    create_chassis(game_state, x=10, y=12, player_id=2, is_human=False)

    movement_system.set_target(game_state, unit_id, 10, 12)

    for _ in range(40):
        movement_system.update(game_state, dt=0.1)

    log_events = _drain_log_events(game_state)
    assert len(log_events) == 1, "Expected exactly one stuck ping per order"
    assert "another unit" in log_events[0]["text"].lower() or "stuck" in log_events[0]["text"].lower()


def test_chassis_does_not_ping_for_ai_owned_units(game_state, movement_system):
    """Only the human player gets pinged about their own stuck units."""
    unit_id = create_chassis(game_state, x=10, y=10, player_id=2, is_human=False)
    create_chassis(game_state, x=10, y=12, player_id=2, is_human=False)

    movement_system.set_target(game_state, unit_id, 10, 12)
    for _ in range(40):
        movement_system.update(game_state, dt=0.1)

    assert _drain_log_events(game_state) == []


def test_new_order_resets_stuck_notification(game_state, movement_system):
    """A fresh move command clears the rate-limit so the player can be
    pinged again for the next order if it also fails."""
    unit_id = create_chassis(game_state, x=10, y=10, player_id=1, is_human=True)
    create_chassis(game_state, x=10, y=12, player_id=2, is_human=False)

    movement_system.set_target(game_state, unit_id, 10, 12)
    for _ in range(40):
        movement_system.update(game_state, dt=0.1)
    assert len(_drain_log_events(game_state)) == 1

    # Issue another impossible order; should be pinged again.
    movement_system.set_target(game_state, unit_id, 10, 12)
    for _ in range(40):
        movement_system.update(game_state, dt=0.1)
    assert len(_drain_log_events(game_state)) == 2
