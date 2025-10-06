from . import config

# TODO: Integrate logger for debug mode. Currently not used.
#       Not exactly sure how to do so here without spamming.


class Camera:
    """Manages the game's viewport, handling position and zoom.

    The camera determines which part of the game world is visible on the screen.
    It supports panning (moving the position) and zooming.

    Attributes:
        x (float): The x-coordinate of the camera's top-left corner in world space.
        y (float): The y-coordinate of the camera's top-left corner in world space.
        zoom (float): The current zoom level.
        min_zoom (float): The minimum allowed zoom level.
        max_zoom (float): The maximum allowed zoom level.
    """

    def __init__(self, x=0, y=0, zoom=1.0, min_zoom=0.5, max_zoom=2.0):
        """Initializes the Camera.

        Args:
            x: The initial x-coordinate.
            y: The initial y-coordinate.
            zoom: The initial zoom level.
            min_zoom: The minimum zoom level.
            max_zoom: The maximum zoom level.
        """
        self.x = x
        self.y = y
        self.zoom = zoom
        self.min_zoom = min_zoom
        self.max_zoom = max_zoom

    def move(self, dx, dy):
        """Moves the camera by a given delta.

        Args:
            dx (float): The change in the x-coordinate.
            dy (float): The change in the y-coordinate.
        """
        self.x += dx
        self.y += dy

    def set_position(self, x, y):
        """Sets the camera's position to specific coordinates.

        Args:
            x (float): The new x-coordinate.
            y (float): The new y-coordinate.
        """
        self.x = x
        self.y = y

    def zoom_in(self, amount=0.1):
        """Increases the zoom level by a given amount.

        Args:
            amount (float): The amount to increase the zoom by.
        """
        self.zoom = min(self.max_zoom, self.zoom + amount)

    def zoom_out(self, amount=0.1):
        """Decreases the zoom level by a given amount.

        Args:
            amount (float): The amount to decrease the zoom by.
        """
        self.zoom = max(self.min_zoom, self.zoom - amount)

    def set_zoom(self, zoom):
        """Sets the zoom level to a specific value, clamping it within limits.

        Args:
            zoom (float): The new zoom level.
        """
        self.zoom = max(self.min_zoom, min(self.max_zoom, zoom))

    def screen_to_grid(self, screen_x: int, screen_y: int) -> tuple[int, int]:
        """Converts screen pixel coordinates to world grid coordinates.

        This method takes a pixel coordinate from the screen and transforms it
        into a grid coordinate in the game world, accounting for the camera's
        position and zoom level.

        Args:
            screen_x: The x-coordinate on the screen.
            screen_y: The y-coordinate on the screen.

        Returns:
            A tuple (x, y) representing the corresponding grid coordinates.
        """
        world_grid_x = (screen_x / self.zoom) / config.GRID_SIZE + self.x
        world_grid_y = (screen_y / self.zoom) / config.GRID_SIZE + self.y
        return int(world_grid_x), int(world_grid_y)
