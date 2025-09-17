import pygame
import pytest
from unittest.mock import MagicMock, patch

from command_line_conflict.systems.ui_system import UISystem
from command_line_conflict.game_state import GameState
from command_line_conflict.camera import Camera
from command_line_conflict.components.position import Position
from command_line_conflict.components.attack import Attack
from command_line_conflict.components.selectable import Selectable
from command_line_conflict.components.renderable import Renderable
from command_line_conflict.config import GRID_SIZE


from command_line_conflict.maps.base import Map


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
            Selectable: selectable,
            Renderable: Renderable(icon="T", color=(255, 255, 255)),
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


@patch("pygame.draw.line")
def test_draw_attack_range_with_camera_offset(
    mock_draw_line, ui_system, game_state
):
    """Test that the attack range circle is drawn correctly with camera offset."""
    ui_system.camera.x = 5
    ui_system.camera.y = 5

    ui_system.draw(game_state, paused=False)

    # Expected center with camera offset
    expected_center_x = (10 - 5) * GRID_SIZE + GRID_SIZE / 2
    expected_center_y = (10 - 5) * GRID_SIZE + GRID_SIZE / 2
    radius = 5 * GRID_SIZE

    # Check that draw.line was called (for the dotted circle)
    assert mock_draw_line.called

    # Check the center of the circle from the first call to draw.line
    first_call_args = mock_draw_line.call_args_list[0][0]
    start_pos = first_call_args[2]
    # The center can be approximated from the start_pos of the first dash
    # For a circle with 30 dashes, the first dash starts at angle 0
    # So, start_pos should be (center_x + radius, center_y)
    assert start_pos[0] == pytest.approx(expected_center_x + radius, 1)
    assert start_pos[1] == pytest.approx(expected_center_y, 1)


@patch("pygame.draw.line")
def test_draw_attack_range_with_camera_zoom(mock_draw_line, ui_system, game_state):
    """Test that the attack range circle is drawn correctly with camera zoom."""
    ui_system.camera.zoom = 1.5

    ui_system.draw(game_state, paused=False)

    # Expected center and radius with camera zoom
    zoom = 1.5
    zoomed_grid_size = GRID_SIZE * zoom
    expected_center_x = 10 * zoomed_grid_size + zoomed_grid_size / 2
    expected_center_y = 10 * zoomed_grid_size + zoomed_grid_size / 2
    radius = 5 * zoomed_grid_size

    # Check that draw.line was called
    assert mock_draw_line.called

    # Check the center of the circle from the first call to draw.line
    first_call_args = mock_draw_line.call_args_list[0][0]
    start_pos = first_call_args[2]
    assert start_pos[0] == pytest.approx(expected_center_x + radius, 1)
    assert start_pos[1] == pytest.approx(expected_center_y, 1)
