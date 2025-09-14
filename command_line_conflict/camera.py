from . import config


class Camera:
    def __init__(self, x=0, y=0, zoom=1.0, min_zoom=0.5, max_zoom=2.0):
        self.x = x
        self.y = y
        self.zoom = zoom
        self.min_zoom = min_zoom
        self.max_zoom = max_zoom

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def zoom_in(self, amount=0.1):
        self.zoom = min(self.max_zoom, self.zoom + amount)

    def zoom_out(self, amount=0.1):
        self.zoom = max(self.min_zoom, self.zoom - amount)

    def set_zoom(self, zoom):
        self.zoom = max(self.min_zoom, min(self.max_zoom, zoom))

    def screen_to_grid(self, screen_x: int, screen_y: int) -> tuple[int, int]:
        """Converts screen pixel coordinates to world grid coordinates."""
        world_grid_x = (screen_x / self.zoom) / config.GRID_SIZE + self.x
        world_grid_y = (screen_y / self.zoom) / config.GRID_SIZE + self.y
        return int(world_grid_x), int(world_grid_y)
