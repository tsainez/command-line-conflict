import pytest
from hypothesis import given
from hypothesis import strategies as st

from command_line_conflict import config
from command_line_conflict.components.position import Position
from command_line_conflict.game_state import GameState
from command_line_conflict.maps.simple_map import SimpleMap


@pytest.fixture
def game_state():
    return GameState(SimpleMap())


# Test entity creation unique IDs
@given(st.integers(min_value=1, max_value=100))
def test_create_entity_unique_ids(n):
    game_state = GameState(SimpleMap())
    ids = set()
    # Limit n to be within MAX_ENTITIES to avoid RuntimeError
    n = min(n, config.MAX_ENTITIES)
    for _ in range(n):
        entity_id = game_state.create_entity()
        assert entity_id not in ids
        ids.add(entity_id)


# Test spatial map consistency
@given(
    st.floats(min_value=0, max_value=100, allow_nan=False, allow_infinity=False),
    st.floats(min_value=0, max_value=100, allow_nan=False, allow_infinity=False),
    st.floats(min_value=0, max_value=100, allow_nan=False, allow_infinity=False),
    st.floats(min_value=0, max_value=100, allow_nan=False, allow_infinity=False),
)
def test_update_entity_position_consistency(x1, y1, x2, y2):
    game_state = GameState(SimpleMap())
    entity_id = game_state.create_entity()

    # Initial position
    pos_component = Position(x1, y1)
    game_state.add_component(entity_id, pos_component)

    # Verify initial spatial map
    ix1, iy1 = int(x1), int(y1)
    assert entity_id in game_state.spatial_map.get((ix1, iy1), set())

    # Update position
    game_state.update_entity_position(entity_id, x2, y2)

    # Verify new position in component
    pos = game_state.get_component(entity_id, Position)
    assert pos.x == x2
    assert pos.y == y2

    # Verify spatial map update
    ix2, iy2 = int(x2), int(y2)
    assert entity_id in game_state.spatial_map.get((ix2, iy2), set())

    # If moved to a different cell, should verify it's not in the old cell
    if (ix1, iy1) != (ix2, iy2):
        assert entity_id not in game_state.spatial_map.get((ix1, iy1), set())


# Test position occupied check
@given(
    st.floats(min_value=0, max_value=100, allow_nan=False, allow_infinity=False),
    st.floats(min_value=0, max_value=100, allow_nan=False, allow_infinity=False),
)
def test_is_position_occupied(x, y):
    game_state = GameState(SimpleMap())
    entity_id = game_state.create_entity()
    game_state.add_component(entity_id, Position(x, y))

    ix, iy = int(x), int(y)

    # Should be occupied
    assert game_state.is_position_occupied(ix, iy)

    # Should not be occupied if we exclude the entity
    assert not game_state.is_position_occupied(ix, iy, exclude_entity_id=entity_id)

    # Another position should be empty
    if ix > 0:
        assert not game_state.is_position_occupied(ix - 1, iy)
