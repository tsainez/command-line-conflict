from unittest.mock import Mock, patch

import pygame
import pytest

from command_line_conflict import config
from command_line_conflict.camera import Camera
from command_line_conflict.components.position import Position
from command_line_conflict.components.renderable import Renderable
from command_line_conflict.game_state import GameState
from command_line_conflict.systems.rendering_system import RenderingSystem


@pytest.fixture
def rendering_setup():
    mock_screen = Mock()
    mock_screen.get_width.return_value = 800
    mock_screen.get_height.return_value = 600

    mock_font = Mock()
    mock_surface = Mock()
    # Need to return a surface that can be scaled
    mock_surface.copy.return_value = mock_surface
    mock_font.render.return_value = mock_surface

    # Camera at (10, 10), zoom 1.0. Viewport is 800x600 px. Grid is 20px.
    # Visible width in tiles = 800 / 20 = 40 tiles.
    # Visible height in tiles = 600 / 20 = 30 tiles.
    # Visible range approx: x=[10, 50], y=[10, 40]
    # With padding +/- 2: min_x=8, min_y=8, max_x=52, max_y=42
    camera = Camera(x=10, y=10, zoom=1.0)

    rendering_system = RenderingSystem(
        screen=mock_screen, font=mock_font, camera=camera
    )

    mock_map = Mock()
    game_state = GameState(game_map=mock_map)

    return rendering_system, game_state, mock_screen, mock_font


def test_culling_skips_offscreen_entities(rendering_setup):
    rendering_system, game_state, mock_screen, mock_font = rendering_setup

    # Entity inside view (e.g. at 20, 20)
    visible_id = game_state.create_entity()
    game_state.add_component(visible_id, Position(20, 20))
    game_state.add_component(visible_id, Renderable("V"))

    # Entity outside view (e.g. at 0, 0) -> < 8 (min_x)
    invisible_id = game_state.create_entity()
    game_state.add_component(invisible_id, Position(0, 0))
    game_state.add_component(invisible_id, Renderable("I"))

    # Act
    with patch("pygame.transform.scale", return_value=Mock()):
        rendering_system.draw(game_state, paused=False)

    # Assert
    # Verify "V" was rendered
    calls = mock_font.render.call_args_list
    assert any(args[0][0] == "V" for args in calls)

    # Verify "I" was NOT rendered
    assert not any(args[0][0] == "I" for args in calls)


def test_culling_includes_entities_near_edge(rendering_setup):
    rendering_system, game_state, mock_screen, mock_font = rendering_setup

    # Padding is 2 tiles.
    # min_x = 10 - 2 = 8.

    # Entity at 8, 20 should be visible
    edge_id = game_state.create_entity()
    game_state.add_component(edge_id, Position(8, 20))
    game_state.add_component(edge_id, Renderable("E"))

    # Entity at 7, 20 should be invisible
    outside_id = game_state.create_entity()
    game_state.add_component(outside_id, Position(7, 20))
    game_state.add_component(outside_id, Renderable("O"))

    # Act
    with patch("pygame.transform.scale", return_value=Mock()):
        rendering_system.draw(game_state, paused=False)

    # Assert
    calls = mock_font.render.call_args_list
    assert any(args[0][0] == "E" for args in calls)
    assert not any(args[0][0] == "O" for args in calls)
