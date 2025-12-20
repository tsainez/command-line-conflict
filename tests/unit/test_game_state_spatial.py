from command_line_conflict.components.position import Position
from command_line_conflict.game_state import GameState
from command_line_conflict.maps.base import Map


def test_spatial_map_operations():
    game_map = Map(10, 10)
    game_state = GameState(game_map)

    # 1. Add entity
    e1 = game_state.create_entity()
    game_state.add_component(e1, Position(5, 5))

    # Check if spatial map is populated
    entities = game_state.get_entities_at_position(5, 5)
    assert e1 in entities
    assert len(entities) == 1
    assert (5, 5) in game_state.spatial_map
    assert e1 in game_state.spatial_map[(5, 5)]

    # 2. Add second entity at same pos
    e2 = game_state.create_entity()
    game_state.add_component(e2, Position(5, 5))

    entities = game_state.get_entities_at_position(5, 5)
    assert len(entities) == 2
    assert e1 in entities
    assert e2 in entities

    # 3. Move e1
    game_state.update_entity_position(e1, 6.5, 6.5)  # Should map to 6, 6

    # e1 should be at 6,6; e2 should stay at 5,5
    entities_at_5_5 = game_state.get_entities_at_position(5, 5)
    assert len(entities_at_5_5) == 1
    assert entities_at_5_5[0] == e2

    entities_at_6_6 = game_state.get_entities_at_position(6, 6)
    assert len(entities_at_6_6) == 1
    assert entities_at_6_6[0] == e1

    pos_comp = game_state.get_component(e1, Position)
    assert pos_comp.x == 6.5
    assert pos_comp.y == 6.5

    # 4. Remove e2
    game_state.remove_entity(e2)
    assert game_state.get_entities_at_position(5, 5) == []
    assert (5, 5) not in game_state.spatial_map  # cleanup empty key

    # 5. Move e1 to new location and remove via remove_component
    game_state.update_entity_position(e1, 7, 7)
    assert game_state.get_entities_at_position(7, 7) == [e1]

    game_state.remove_component(e1, Position)
    assert game_state.get_entities_at_position(7, 7) == []
