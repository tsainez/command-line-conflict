from . import config

# TODO: Integrate logger for debug mode. Currently not used.
#       Not exactly sure how to do so here without spamming.


class Camera:
    """Manages the viewport of the game world."""

    def __init__(
        self,
        x: float = 0,
        y: float = 0,
        zoom: float = 1.0,
        min_zoom: float = 0.5,
        max_zoom: float = 2.0,
    ):
        """Initializes the Camera.

        Args:
            x: The initial x-coordinate of the camera (in grid units).
            y: The initial y-coordinate of the camera (in grid units).
            zoom: The initial zoom level.
            min_zoom: The minimum allowed zoom level.
            max_zoom: The maximum allowed zoom level.
        """
        self.x = x
        self.y = y
        self.zoom = zoom
        self.min_zoom = min_zoom
        self.max_zoom = max_zoom

    def move(self, dx: float, dy: float) -> None:
        """Moves the camera by a delta amount.

        Args:
            dx: The change in x-coordinate (in grid units).
            dy: The change in y-coordinate (in grid units).
        """
        self.x += dx
        self.y += dy

    def set_position(self, x: float, y: float) -> None:
        """Sets the camera's position directly.

        Args:
            x: The new x-coordinate (in grid units).
            y: The new y-coordinate (in grid units).
        """
        self.x = x
        self.y = y

    def zoom_in(self, amount: float = 0.1) -> None:
        """Zooms the camera in.

        Args:
            amount: The amount to increase the zoom level by.
        """
        self.zoom = min(self.max_zoom, self.zoom + amount)

    def zoom_out(self, amount: float = 0.1) -> None:
        """Zooms the camera out.

        Args:
            amount: The amount to decrease the zoom level by.
        """
        self.zoom = max(self.min_zoom, self.zoom - amount)

    def set_zoom(self, zoom: float) -> None:
        """Sets the zoom level directly, clamped between min and max zoom.

        Args:
            zoom: The target zoom level.
        """
        self.zoom = max(self.min_zoom, min(self.max_zoom, zoom))

    def screen_to_grid(self, screen_x: int, screen_y: int) -> tuple[int, int]:
        """Converts screen pixel coordinates to world grid coordinates.

        Args:
            screen_x: The x-coordinate on the screen in pixels.
            screen_y: The y-coordinate on the screen in pixels.

        Returns:
            tuple[int, int]: The corresponding (x, y) coordinates in the world grid.
        """
        world_grid_x = (screen_x / self.zoom) / config.GRID_SIZE + self.x
        world_grid_y = (screen_y / self.zoom) / config.GRID_SIZE + self.y
        return int(world_grid_x), int(world_grid_y)
