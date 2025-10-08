from .base import Map


class SimpleMap(Map):
    """A simple map enclosed by walls."""

    def __init__(self) -> None:
        """Initializes the SimpleMap and adds a border of walls."""
        super().__init__(width=60, height=60)

        # Add top and bottom walls
        for x in range(self.width):
            self.add_wall(x, 0)
            self.add_wall(x, self.height - 1)

        # Add left and right walls
        for y in range(1, self.height - 1):
            self.add_wall(0, y)
            self.add_wall(self.width - 1, y)