from unittest.mock import Mock, call, patch

import pygame

from command_line_conflict import config
from command_line_conflict.camera import Camera
from command_line_conflict.components.health import Health
from command_line_conflict.components.position import Position
from command_line_conflict.components.renderable import Renderable
from command_line_conflict.game_state import GameState
from command_line_conflict.systems.rendering_system import RenderingSystem


@patch("pygame.draw.rect")
@patch("pygame.transform.scale")
def test_health_bar_colors(mock_scale, mock_draw_rect):
    """Verify health bar changes color based on health percentage."""
    # Arrange
    mock_screen = Mock()
    mock_screen.get_width.return_value = 800
    mock_screen.get_height.return_value = 600
    mock_font = Mock()
    mock_surface = Mock()
    mock_scale.return_value = Mock()
    mock_font.render.return_value = mock_surface

    camera = Camera(x=0, y=0, zoom=1.0)
    rendering_system = RenderingSystem(
        screen=mock_screen, font=mock_font, camera=camera
    )

    mock_map = Mock()
    game_state = GameState(game_map=mock_map)
    entity_id = game_state.create_entity()

    game_state.add_component(entity_id, Position(x=10, y=10))
    game_state.add_component(entity_id, Renderable(icon="U"))

    # Helper to check call args for a specific color
    def assert_color_used(color):
        found = False
        for call_args in mock_draw_rect.call_args_list:
            # call_args is (args, kwargs)
            # args[1] is the color
            if call_args[0][1] == color:
                found = True
                break
        assert found, f"Color {color} was not used in any draw.rect call"

    # Test Case 1: High Health (Green)
    game_state.add_component(entity_id, Health(hp=80, max_hp=100))
    mock_draw_rect.reset_mock()
    rendering_system.draw(game_state, paused=False)
    assert_color_used((0, 255, 0))  # Green

    # Test Case 2: Medium Health (Yellow)
    # We need to overwrite the component
    game_state.add_component(entity_id, Health(hp=40, max_hp=100))
    mock_draw_rect.reset_mock()
    rendering_system.draw(game_state, paused=False)
    assert_color_used((255, 255, 0))  # Yellow

    # Test Case 3: Low Health (Red)
    game_state.add_component(entity_id, Health(hp=20, max_hp=100))
    mock_draw_rect.reset_mock()
    rendering_system.draw(game_state, paused=False)
    assert_color_used((255, 0, 0))  # Red

    # Test Case 4: Border and Background are always drawn
    # Background (Dark Grey)
    assert_color_used((60, 60, 60))
    # Border (Black)
    assert_color_used((0, 0, 0))
