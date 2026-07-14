from command_line_conflict.components.dead import Dead
from command_line_conflict.components.factory import Factory
from command_line_conflict.components.movable import Movable
from command_line_conflict.components.player import Player
from command_line_conflict.components.position import Position
from command_line_conflict.components.selectable import Selectable
from command_line_conflict.game_state import GameState
from command_line_conflict.maps.simple_map import SimpleMap
from command_line_conflict.systems.control_group_system import ControlGroupSystem


def make_unit(game_state: GameState, x: float, y: float, player_id: int = 1, selected: bool = True) -> int:
    """Creates a mobile, selectable "unit" (has Movable)."""
    entity_id = game_state.create_entity()
    game_state.add_component(entity_id, Position(x, y))
    game_state.add_component(entity_id, Movable(speed=1.0))
    game_state.add_component(entity_id, Selectable())
    game_state.add_component(entity_id, Player(player_id=player_id))
    game_state.entities[entity_id][Selectable].is_selected = selected
    return entity_id


def make_building(game_state: GameState, x: float, y: float, player_id: int = 1, selected: bool = True) -> int:
    """Creates a stationary, selectable "building" (no Movable)."""
    entity_id = game_state.create_entity()
    game_state.add_component(entity_id, Position(x, y))
    game_state.add_component(entity_id, Factory(input_unit="chassis", output_unit="rover"))
    game_state.add_component(entity_id, Selectable())
    game_state.add_component(entity_id, Player(player_id=player_id))
    game_state.entities[entity_id][Selectable].is_selected = selected
    return entity_id


def make_state() -> GameState:
    return GameState(SimpleMap())


def test_assign_and_select_group_round_trip():
    game_state = make_state()
    system = ControlGroupSystem()
    unit_a = make_unit(game_state, 0, 0)
    unit_b = make_unit(game_state, 2, 2)

    assigned = system.assign_group(game_state, 1, player_id=1)
    assert assigned == {unit_a, unit_b}

    # Deselect everything, then recall the group.
    game_state.entities[unit_a][Selectable].is_selected = False
    game_state.entities[unit_b][Selectable].is_selected = False

    selected = system.select_group(game_state, 1, player_id=1)
    assert set(selected) == {unit_a, unit_b}
    assert game_state.entities[unit_a][Selectable].is_selected is True
    assert game_state.entities[unit_b][Selectable].is_selected is True


def test_assigning_empty_selection_assigns_nothing():
    game_state = make_state()
    system = ControlGroupSystem()
    make_unit(game_state, 0, 0, selected=False)

    assigned = system.assign_group(game_state, 1, player_id=1)
    assert assigned == set()
    assert not system.select_group(game_state, 1, player_id=1)


def test_at_least_ten_group_slots_are_independent():
    game_state = make_state()
    system = ControlGroupSystem()

    entity_ids = []
    for i in range(10):
        eid = make_unit(game_state, i, i, selected=True)
        entity_ids.append(eid)
        assigned = system.assign_group(game_state, i + 1, player_id=1)
        assert assigned == {eid}
        game_state.entities[eid][Selectable].is_selected = False

    for i in range(10):
        selected = system.select_group(game_state, i + 1, player_id=1)
        assert selected == [entity_ids[i]]
        game_state.entities[entity_ids[i]][Selectable].is_selected = False


def test_selecting_group_replaces_current_selection():
    game_state = make_state()
    system = ControlGroupSystem()
    grouped = make_unit(game_state, 0, 0, selected=True)
    system.assign_group(game_state, 1, player_id=1)

    other = make_unit(game_state, 5, 5, selected=True)
    game_state.entities[grouped][Selectable].is_selected = False

    system.select_group(game_state, 1, player_id=1)

    assert game_state.entities[grouped][Selectable].is_selected is True
    assert game_state.entities[other][Selectable].is_selected is False


def test_only_one_building_allowed_per_group():
    game_state = make_state()
    system = ControlGroupSystem()
    building_1 = make_building(game_state, 0, 0)
    building_2 = make_building(game_state, 1, 1)
    unit = make_unit(game_state, 2, 2)

    assigned = system.assign_group(game_state, 1, player_id=1)

    assert unit in assigned
    assert building_1 in assigned
    assert building_2 not in assigned
    assert len(assigned) == 2


def test_group_is_scoped_to_a_single_player():
    game_state = make_state()
    system = ControlGroupSystem()
    p1_unit = make_unit(game_state, 0, 0, player_id=1, selected=True)
    make_unit(game_state, 1, 1, player_id=2, selected=True)

    assigned = system.assign_group(game_state, 1, player_id=1)
    assert assigned == {p1_unit}

    # Player 2 has nothing bound to group 1.
    assert not system.select_group(game_state, 1, player_id=2)


def test_dead_or_removed_entities_are_pruned_from_group():
    game_state = make_state()
    system = ControlGroupSystem()
    alive = make_unit(game_state, 0, 0)
    dying = make_unit(game_state, 1, 1)
    removed = make_unit(game_state, 2, 2)

    system.assign_group(game_state, 1, player_id=1)

    game_state.add_component(dying, Dead())
    game_state.remove_entity(removed)

    selected = system.select_group(game_state, 1, player_id=1)
    assert selected == [alive]


def test_get_center_position_returns_centroid():
    game_state = make_state()
    system = ControlGroupSystem()
    a = make_unit(game_state, 0, 0)
    b = make_unit(game_state, 4, 2)

    center = system.get_center_position(game_state, [a, b])
    assert center == (2.0, 1.0)


def test_get_center_position_returns_none_when_no_positions():
    game_state = make_state()
    system = ControlGroupSystem()
    assert system.get_center_position(game_state, []) is None
