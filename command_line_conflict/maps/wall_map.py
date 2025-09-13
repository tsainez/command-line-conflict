from .base import Map


class WallMap(Map):
    """A small map with a horizontal wall to demonstrate pathfinding."""

    def __init__(self) -> None:
        """Initializes the WallMap and creates a horizontal wall with a gap."""
        super().__init__(width=20, height=15)
        # create a simple horizontal wall with a gap
        for x in range(3, 17):
            if x != 10:
                self.add_wall(x, 7)
