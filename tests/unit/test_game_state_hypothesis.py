from hypothesis import given
from hypothesis import strategies as st

from command_line_conflict.components.health import Health
from command_line_conflict.components.position import Position
from command_line_conflict.game_state import GameState
from command_line_conflict.maps.simple_map import SimpleMap


@given(st.lists(st.tuples(st.integers(min_value=0, max_value=100), st.integers(min_value=0, max_value=100))))
def test_entity_creation_and_retrieval(positions):
    game_map = SimpleMap()
    game_state = GameState(game_map)

    entity_ids = []
    for x, y in positions:
        # Avoid hitting max entities limit in test
        if len(entity_ids) >= 1000:
            break

        eid = game_state.create_entity()
        entity_ids.append(eid)
        game_state.add_component(eid, Position(x, y))

    # Check that all entities have unique IDs
    assert len(set(entity_ids)) == len(entity_ids)

    # Check that we can retrieve Position for all entities
    for eid in entity_ids:
        pos = game_state.get_component(eid, Position)
        assert pos is not None

    # Check get_entities_with_component
    with_pos = game_state.get_entities_with_component(Position)
    assert len(with_pos) == len(entity_ids)
    assert with_pos == set(entity_ids)


@given(st.integers(min_value=1, max_value=50))
def test_remove_entity(num_entities):
    game_map = SimpleMap()
    game_state = GameState(game_map)

    entities = []
    for _ in range(num_entities):
        eid = game_state.create_entity()
        game_state.add_component(eid, Health(10, 10))
        entities.append(eid)

    # Remove half
    to_remove = entities[: num_entities // 2]
    for eid in to_remove:
        game_state.remove_entity(eid)

    # Check they are gone
    for eid in to_remove:
        assert eid not in game_state.entities

    # Check remaining
    remaining = entities[num_entities // 2 :]
    for eid in remaining:
        assert eid in game_state.entities
        assert game_state.get_component(eid, Health) is not None
