from command_line_conflict import config
from command_line_conflict.camera import Camera


def test_screen_to_grid():
    # Arrange
    camera = Camera(x=10, y=20, zoom=2.0)
    # Let's choose screen coordinates that result in integer grid coordinates
    # to avoid floating point issues.
    # Let's say we want to find the screen coordinates for grid cell (21, 27)
    # screen_x = (21 - 10) * 20 * 2.0 = 11 * 40 = 440
    # screen_y = (27 - 20) * 20 * 2.0 = 7 * 40 = 280
    screen_x, screen_y = 440, 280

    expected_grid_x = 21
    expected_grid_y = 27

    # Act
    grid_x, grid_y = camera.screen_to_grid(screen_x, screen_y)

    # Assert
    # Let's trace the calculation in the implementation:
    # grid_x = (440 / 2.0) / 20 + 10 = 220 / 20 + 10 = 11 + 10 = 21
    # grid_y = (280 / 2.0) / 20 + 20 = 140 / 20 + 20 = 7 + 20 = 27

    assert grid_x == expected_grid_x
    assert grid_y == expected_grid_y
