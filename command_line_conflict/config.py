"""This file contains the main configuration variables for the game.

This module defines global constants and settings used throughout the game,
such as screen dimensions, frame rate, and gameplay parameters.
"""

# A boolean that turns on/off debug mode.
DEBUG = False

# The width of the screen in pixels.
SCREEN_WIDTH = 800
# The height of the screen in pixels.
SCREEN_HEIGHT = 600
# A dictionary containing the screen width and height.
SCREEN = {
    "width": SCREEN_WIDTH,
    "height": SCREEN_HEIGHT,
}

# The size of each grid cell in pixels.
GRID_SIZE = 20
# The target frames per second for the game.
FPS = 60
# The speed of the camera movement.
CAMERA_SPEED = 10

# A dictionary mapping player IDs to their colors.
PLAYER_COLORS = {
    1: (0, 128, 255),  # Blue
    2: (255, 0, 0),  # Red
}
