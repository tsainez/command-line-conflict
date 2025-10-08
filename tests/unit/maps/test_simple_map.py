from unittest.mock import Mock, call, patch

import pygame

from command_line_conflict import config
from command_line_conflict.camera import Camera
from command_line_conflict.maps.simple_map import SimpleMap


@patch("pygame.transform.scale")
def test_map_draw_with_camera(mock_scale):
    # Arrange
    mock_surf = Mock()
    mock_font = Mock()
    mock_surface = Mock()
    mock_scaled_surface = Mock()
    mock_font.render.return_value = mock_surface
    mock_scale.return_value = mock_scaled_surface

    camera = Camera(x=10, y=5, zoom=2.0)
    game_map = SimpleMap()
    game_map.add_wall(15, 20)

    # Act
    game_map.draw(mock_surf, mock_font, camera)

    # Assert
    expected_x = (15 - camera.x) * config.GRID_SIZE * camera.zoom
    expected_y = (20 - camera.y) * config.GRID_SIZE * camera.zoom

    grid_size = int(config.GRID_SIZE * camera.zoom)
    mock_scale.assert_any_call(mock_surface, (grid_size, grid_size))
    mock_surf.blit.assert_any_call(
        mock_scaled_surface, (expected_x, expected_y)
    )


def test_simple_map_has_border_walls():
    """Tests that the SimpleMap is correctly enclosed by walls."""
    game_map = SimpleMap()

    # Check a few points on each wall
    assert game_map.is_blocked(0, 0)  # Top-left corner
    assert game_map.is_blocked(game_map.width - 1, 0)  # Top-right corner
    assert game_map.is_blocked(0, game_map.height - 1)  # Bottom-left corner
    assert game_map.is_blocked(
        game_map.width - 1, game_map.height - 1
    )  # Bottom-right corner
    assert game_map.is_blocked(game_map.width // 2, 0)  # Middle of top wall
    assert game_map.is_blocked(
        game_map.width // 2, game_map.height - 1
    )  # Middle of bottom wall
    assert game_map.is_blocked(0, game_map.height // 2)  # Middle of left wall
    assert game_map.is_blocked(
        game_map.width - 1, game_map.height // 2
    )  # Middle of right wall

    # Check a point in the middle is not a wall
    assert not game_map.is_blocked(game_map.width // 2, game_map.height // 2)


@patch("pygame.transform.scale")
def test_map_draw_without_camera_bug(mock_scale):
    # Arrange
    mock_surf = Mock()
    mock_font = Mock()
    mock_surface = Mock()
    mock_scaled_surface = Mock()
    mock_font.render.return_value = mock_surface
    mock_scale.return_value = mock_scaled_surface

    game_map = SimpleMap()
    game_map.add_wall(15, 20)

    # Act
    game_map.draw(mock_surf, mock_font)

    # Assert
    expected_x = 15 * config.GRID_SIZE
    expected_y = 20 * config.GRID_SIZE

    mock_scale.assert_any_call(
        mock_surface, (config.GRID_SIZE, config.GRID_SIZE)
    )
    mock_surf.blit.assert_any_call(
        mock_scaled_surface, (expected_x, expected_y)
    )