
import pytest
from hypothesis import given, strategies as st
from command_line_conflict.maps.base import Map

# Strategy for map dimensions
map_dims = st.integers(min_value=5, max_value=50)

@st.composite
def map_and_points(draw):
    w = draw(map_dims)
    h = draw(map_dims)
    m = Map(w, h)

    # Generate some walls
    # We don't want too many walls or pathfinding might always fail
    # Use a set to avoid duplicate adds
    wall_coords = draw(st.lists(
        st.tuples(st.integers(0, w-1), st.integers(0, h-1)),
        max_size=(w*h)//2,
        unique=True
    ))

    for x, y in wall_coords:
        m.add_wall(x, y)

    start = (draw(st.integers(min_value=0, max_value=w-1)),
             draw(st.integers(min_value=0, max_value=h-1)))
    goal = (draw(st.integers(min_value=0, max_value=w-1)),
            draw(st.integers(min_value=0, max_value=h-1)))

    return m, start, goal

@given(map_and_points())
def test_pathfinding_properties(data):
    game_map, start, goal = data

    # We are testing non-flying movement
    path = game_map.find_path(start, goal, can_fly=False)

    if not path:
        # If no path, verify that either start/goal is blocked, or they are disconnected.
        # It's hard to verify disconnection efficiently without reimplementing pathfinding.
        # But we can verify that IF start or goal is blocked, path must be empty.
        if game_map.is_blocked(*start) or game_map.is_blocked(*goal):
            assert path == []
        return

    # If start == goal, path should be empty
    if start == goal:
        assert path == []
        return

    # Property: Path must end at goal
    assert path[-1] == goal

    # Property: Path must be continuous and valid
    prev = start
    for step in path:
        # Check continuity (Manhattan distance == 1)
        dx = abs(step[0] - prev[0])
        dy = abs(step[1] - prev[1])
        assert dx + dy == 1, f"Path gap or jump from {prev} to {step}"

        # Check validity (not walking through walls)
        assert not game_map.is_blocked(*step), f"Path goes through wall at {step}"

        prev = step
