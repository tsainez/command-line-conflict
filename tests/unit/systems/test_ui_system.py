from unittest.mock import MagicMock, patch

import pygame
import pytest

from command_line_conflict.camera import Camera
from command_line_conflict.components.attack import Attack
from command_line_conflict.components.detection import Detection
from command_line_conflict.components.position import Position
from command_line_conflict.components.selectable import Selectable
from command_line_conflict.config import GRID_SIZE
from command_line_conflict.game_state import GameState
from command_line_conflict.maps.base import Map
from command_line_conflict.systems.ui_system import UISystem


@pytest.fixture
def game_state():
    """Fixture for creating a mock game state."""
    game_map = MagicMock(spec=Map)
    game_state = GameState(game_map)
    selectable = Selectable()
    selectable.is_selected = True
    game_state.entities = {
        1: {
            Position: Position(10, 10),
            Attack: Attack(attack_damage=10, attack_range=5, attack_speed=1),
            Detection: Detection(detection_range=5),
            Selectable: selectable,
        }
    }
    return game_state


@pytest.fixture
def ui_system():
    """Fixture for creating a UISystem with a mock screen and camera."""
    pygame.init()
    screen = MagicMock()
    font = MagicMock()
    camera = Camera()
    return UISystem(screen, font, camera)


@patch("pygame.draw.rect")
def test_draw_aggregate_attack_range(mock_draw_rect, ui_system, game_state):
    """Test that the aggregate attack range is drawn."""
    ui_system.draw(game_state, paused=False)

    # For a radius of 5, 81 tiles should be in attack range.
    # For a radius of 5, 81 tiles should be in detection range.
    # +1 for the key options panel, +2 for player indicator (box + border)
    assert mock_draw_rect.call_count == 81 + 81 + 1 + 2


@patch("pygame.draw.rect")
def test_draw_aggregate_attack_range_multiple_units(
    mock_draw_rect, ui_system, game_state
):
    """Test that the aggregate attack range is drawn for multiple units."""
    # Add a second unit
    selectable = Selectable()
    selectable.is_selected = True
    game_state.entities[2] = {
        Position: Position(12, 10),
        Attack: Attack(attack_damage=10, attack_range=2, attack_speed=1),
        Detection: Detection(detection_range=2),
        Selectable: selectable,
    }
    game_state.get_component(1, Selectable).is_selected = True

    ui_system.draw(game_state, paused=False)

    # Calculate expected tiles for unit 1 attack (radius 5)
    attack_tiles_1 = set()
    unit_1_pos = (10, 10)
    radius_1 = 5
    for x in range(unit_1_pos[0] - radius_1, unit_1_pos[0] + radius_1 + 1):
        for y in range(unit_1_pos[1] - radius_1, unit_1_pos[1] + radius_1 + 1):
            if (x - unit_1_pos[0]) ** 2 + (y - unit_1_pos[1]) ** 2 <= radius_1**2:
                attack_tiles_1.add((x, y))

    # Calculate expected tiles for unit 2 attack (radius 2)
    attack_tiles_2 = set()
    unit_2_pos = (12, 10)
    radius_2 = 2
    for x in range(unit_2_pos[0] - radius_2, unit_2_pos[0] + radius_2 + 1):
        for y in range(unit_2_pos[1] - radius_2, unit_2_pos[1] + radius_2 + 1):
            if (x - unit_2_pos[0]) ** 2 + (y - unit_2_pos[1]) ** 2 <= radius_2**2:
                attack_tiles_2.add((x, y))

    # Calculate expected tiles for unit 1 detection (radius 5)
    detection_tiles_1 = set()
    radius_3 = 5
    for x in range(unit_1_pos[0] - radius_3, unit_1_pos[0] + radius_3 + 1):
        for y in range(unit_1_pos[1] - radius_3, unit_1_pos[1] + radius_3 + 1):
            if (x - unit_1_pos[0]) ** 2 + (y - unit_1_pos[1]) ** 2 <= radius_3**2:
                detection_tiles_1.add((x, y))

    # Calculate expected tiles for unit 2 detection (radius 2)
    detection_tiles_2 = set()
    radius_4 = 2
    for x in range(unit_2_pos[0] - radius_4, unit_2_pos[0] + radius_4 + 1):
        for y in range(unit_2_pos[1] - radius_4, unit_2_pos[1] + radius_4 + 1):
            if (x - unit_2_pos[0]) ** 2 + (y - unit_2_pos[1]) ** 2 <= radius_4**2:
                detection_tiles_2.add((x, y))

    # The total number of calls should be the size of the union of the two sets
    total_attack_tiles = len(attack_tiles_1.union(attack_tiles_2))
    total_detection_tiles = len(detection_tiles_1.union(detection_tiles_2))
    # +1 for the key options panel, +2 for player indicator (box + border)
    assert mock_draw_rect.call_count == total_attack_tiles + total_detection_tiles + 1 + 2


@patch("pygame.draw.rect")
def test_draw_observer_detection_range(mock_draw_rect, ui_system, game_state):
    """Test that the observer's detection range is drawn correctly."""
    # Clear existing entities and add an observer
    game_state.entities = {}
    selectable = Selectable()
    selectable.is_selected = True
    game_state.entities[1] = {
        Position: Position(10, 10),
        Detection: Detection(detection_range=15),
        Selectable: selectable,
    }

    ui_system.draw(game_state, paused=False)

    # Calculate expected tiles for observer detection (radius 15)
    detection_tiles = set()
    unit_pos = (10, 10)
    radius = 15
    for x in range(unit_pos[0] - radius, unit_pos[0] + radius + 1):
        for y in range(unit_pos[1] - radius, unit_pos[1] + radius + 1):
            if (x - unit_pos[0]) ** 2 + (y - unit_pos[1]) ** 2 <= radius**2:
                detection_tiles.add((x, y))

    # The total number of calls should be the size of the detection range + 1 for the panel, +2 for player indicator
    assert mock_draw_rect.call_count == len(detection_tiles) + 1 + 2
