import pytest

from command_line_conflict.components.position import Position
from command_line_conflict.game_state import GameState
from command_line_conflict.maps.simple_map import SimpleMap


@pytest.fixture
def populated_game_state():
    """Returns a GameState with 1000 entities."""
    gs = GameState(SimpleMap())
    for i in range(1000):
        eid = gs.create_entity()
        # Distribute them on a 100x100 grid approximately
        gs.add_component(eid, Position(i % 100, i // 100))
    return gs


def test_benchmark_update_entity_position(benchmark):
    gs = GameState(SimpleMap())
    eid = gs.create_entity()
    gs.add_component(eid, Position(0, 0))

    def update_loop():
        # Move back and forth
        gs.update_entity_position(eid, 1, 1)
        gs.update_entity_position(eid, 0, 0)

    benchmark(update_loop)


def test_benchmark_is_position_occupied_hit(benchmark, populated_game_state):
    # (50, 5) should be occupied (50 + 5*100 = 550 < 1000)
    benchmark(populated_game_state.is_position_occupied, 50, 5)


def test_benchmark_is_position_occupied_miss(benchmark, populated_game_state):
    # (200, 200) should be empty
    benchmark(populated_game_state.is_position_occupied, 200, 200)


def test_benchmark_get_entities_at_position(benchmark, populated_game_state):
    # (50, 5) has an entity
    benchmark(populated_game_state.get_entities_at_position, 50, 5)
