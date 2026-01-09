# pylint: disable=redefined-outer-name, protected-access
from unittest.mock import MagicMock, patch

import pytest

from command_line_conflict.components.player import Player
from command_line_conflict.components.position import Position
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


def test_clear_selection(game_state, selection_system):
    """Test that clear_selection deselects all units."""
    unit1 = create_chassis(game_state, 10, 10, 1, is_human=True)
    unit2 = create_chassis(game_state, 12, 12, 1, is_human=True)

    game_state.get_component(unit1, Selectable).is_selected = True
    game_state.get_component(unit2, Selectable).is_selected = True

    selection_system.clear_selection(game_state)

    assert not game_state.get_component(unit1, Selectable).is_selected
    assert not game_state.get_component(unit2, Selectable).is_selected


def test_click_selection_single_unit(game_state, selection_system):
    """Test clicking on a single unit selects it and deselects others."""
    unit1 = create_chassis(game_state, 10, 10, 1, is_human=True)
    unit2 = create_chassis(game_state, 12, 12, 1, is_human=True)

    # Pre-select unit 2
    game_state.get_component(unit2, Selectable).is_selected = True

    # Click on unit 1
    selection_system.handle_click_selection(game_state, (10, 10), shift_pressed=False)

    assert game_state.get_component(unit1, Selectable).is_selected
    assert not game_state.get_component(unit2, Selectable).is_selected


def test_click_selection_shift_add(game_state, selection_system):
    """Test shift-clicking adds to selection."""
    unit1 = create_chassis(game_state, 10, 10, 1, is_human=True)
    unit2 = create_chassis(game_state, 12, 12, 1, is_human=True)

    # Pre-select unit 1
    game_state.get_component(unit1, Selectable).is_selected = True

    # Shift-click on unit 2
    selection_system.handle_click_selection(game_state, (12, 12), shift_pressed=True)

    assert game_state.get_component(unit1, Selectable).is_selected
    assert game_state.get_component(unit2, Selectable).is_selected


def test_click_selection_shift_remove(game_state, selection_system):
    """Test shift-clicking an already selected unit removes it."""
    unit1 = create_chassis(game_state, 10, 10, 1, is_human=True)

    # Pre-select unit 1
    game_state.get_component(unit1, Selectable).is_selected = True

    # Shift-click on unit 1
    selection_system.handle_click_selection(game_state, (10, 10), shift_pressed=True)

    assert not game_state.get_component(unit1, Selectable).is_selected


def test_click_selection_empty_space(game_state, selection_system):
    """Test clicking on empty space clears selection."""
    unit1 = create_chassis(game_state, 10, 10, 1, is_human=True)
    game_state.get_component(unit1, Selectable).is_selected = True

    selection_system.handle_click_selection(game_state, (15, 15), shift_pressed=False)

    assert not game_state.get_component(unit1, Selectable).is_selected


def test_click_selection_enemy_unit(game_state, selection_system):
    """Test that clicking an enemy unit does not select it."""
    # Player 2 unit
    unit2 = create_chassis(game_state, 10, 10, 2, is_human=False)

    selection_system.handle_click_selection(game_state, (10, 10), shift_pressed=False, current_player_id=1)

    assert not game_state.get_component(unit2, Selectable).is_selected


def test_drag_selection_basic(game_state, selection_system):
    """Test basic drag selection."""
    unit1 = create_chassis(game_state, 10, 10, 1, is_human=True)
    unit2 = create_chassis(game_state, 20, 20, 1, is_human=True)  # Outside

    selection_system.update(game_state, (9, 9), (11, 11), shift_pressed=False)

    assert game_state.get_component(unit1, Selectable).is_selected
    assert not game_state.get_component(unit2, Selectable).is_selected


def test_drag_selection_ignores_enemy(game_state, selection_system):
    """Test drag selection ignores enemy units."""
    unit1 = create_chassis(game_state, 10, 10, 2, is_human=False)

    selection_system.update(game_state, (9, 9), (11, 11), shift_pressed=False, current_player_id=1)

    assert not game_state.get_component(unit1, Selectable).is_selected
