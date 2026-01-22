import pytest
from hypothesis import given
from hypothesis import strategies as st

# Ensure mock_pygame fixture is used if it's in conftest
from command_line_conflict.maps.base import Map

# Strategy for valid map dimensions
map_dimensions = st.tuples(
    st.integers(min_value=1, max_value=Map.MAX_MAP_DIMENSION), st.integers(min_value=1, max_value=Map.MAX_MAP_DIMENSION)
)


@given(dims=map_dimensions, walls=st.lists(st.tuples(st.integers(), st.integers())))
def test_map_serialization_roundtrip(dims, walls):
    """Test that a Map can be serialized and deserialized back to an equivalent state."""
    width, height = dims
    game_map = Map(width, height)

    # Add walls that are within bounds
    valid_walls = set()
    for x, y in walls:
        if 0 <= x < width and 0 <= y < height:
            game_map.add_wall(x, y)
            valid_walls.add((x, y))

    # Serialize
    data = game_map.to_dict()

    # Deserialize
    new_map = Map.from_dict(data)

    # Check properties
    assert new_map.width == width
    assert new_map.height == height
    assert new_map.walls == valid_walls
    assert new_map.walls == game_map.walls


@given(dims=map_dimensions, x=st.integers(), y=st.integers())
def test_map_bounds_checks(dims, x, y):
    """Test is_walkable handles out of bounds correctly."""
    width, height = dims
    game_map = Map(width, height)

    is_inside = 0 <= x < width and 0 <= y < height

    if not is_inside:
        assert not game_map.is_walkable(x, y)


@given(dims=map_dimensions)
def test_map_creation_limits(dims):
    """Test map creation respects limits."""
    width, height = dims
    # This should succeed because our strategy respects the limit
    m = Map(width, height)
    assert m.width == width
    assert m.height == height


def test_map_creation_excessive_size():
    """Test that creating a map larger than MAX_MAP_DIMENSION raises ValueError."""
    with pytest.raises(ValueError):
        Map(Map.MAX_MAP_DIMENSION + 1, 10)
