from unittest.mock import Mock, patch

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
    mock_scale.assert_called_once_with(mock_surface, (grid_size, grid_size))
    mock_surf.blit.assert_called_once_with(mock_scaled_surface, (expected_x, expected_y))


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
    # This is what it should be
    expected_x = 15 * config.GRID_SIZE
    expected_y = 20 * config.GRID_SIZE

    # The bug is that it doesn't multiply by GRID_SIZE
    # and doesn't scale the surface.

    # We expect scale to be called with the default grid size
    mock_scale.assert_called_once_with(mock_surface, (config.GRID_SIZE, config.GRID_SIZE))
    # We expect blit to be called with the scaled coordinates
    mock_surf.blit.assert_called_once_with(mock_scaled_surface, (expected_x, expected_y))
