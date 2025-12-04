import pytest

from command_line_conflict.components.selectable import Selectable
from command_line_conflict.factories import create_chassis
from command_line_conflict.game_state import GameState
from command_line_conflict.maps.simple_map import SimpleMap
from command_line_conflict.systems.selection_system import SelectionSystem


@pytest.fixture
def game_state():
    """Provides a fresh game state for each test."""
    return GameState(SimpleMap())


@pytest.fixture
def selection_system():
    """Provides a fresh selection system for each test."""
    return SelectionSystem()


def test_drag_select_with_shift_adds_to_selection(game_state, selection_system):
    """
    Verify that a drag selection with the Shift key held down adds to the
    existing selection and does not deselect currently selected units.
    """
    # Arrange: Create three units.
    unit1_id = create_chassis(game_state, x=10, y=10, player_id=1, is_human=True)
    unit2_id = create_chassis(game_state, x=12, y=12, player_id=1, is_human=True)
    unit3_id = create_chassis(game_state, x=14, y=14, player_id=1, is_human=True)

    # Arrange: Initially select the first unit.
    selectable1 = game_state.get_component(unit1_id, Selectable)
    selectable1.is_selected = True

    # Act: Perform a drag-select over the other two units while holding Shift.
    # We pass the original, unmodified selection_system here to test the failing case.
    selection_system_before_fix = SelectionSystem()
    selection_system_before_fix.update(
        game_state, grid_start=(11, 11), grid_end=(15, 15)
    )

    # Assert: Check that the first unit was deselected (the bug).
    selectable1_after = game_state.get_component(unit1_id, Selectable)
    selectable2_after = game_state.get_component(unit2_id, Selectable)
    selectable3_after = game_state.get_component(unit3_id, Selectable)

    assert not selectable1_after.is_selected
    assert selectable2_after.is_selected
    assert selectable3_after.is_selected

    # Arrange: Reset selection state
    selectable1.is_selected = True
    selectable2_after.is_selected = False
    selectable3_after.is_selected = False

    # Act: Perform the same drag-select, but this time with shift_pressed=True.
    selection_system.update(
        game_state, grid_start=(11, 11), grid_end=(15, 15), shift_pressed=True
    )

    # Assert: All three units should now be selected.
    assert selectable1.is_selected
    assert game_state.get_component(unit2_id, Selectable).is_selected
    assert game_state.get_component(unit3_id, Selectable).is_selected
