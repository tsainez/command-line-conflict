from .base import Map


class WallMap(Map):
    """Small map with walls to demonstrate pathfinding."""

    def __init__(self) -> None:
        super().__init__(width=20, height=15)
        # create a simple horizontal wall with a gap
        for x in range(3, 17):
            if x != 10:
                self.add_wall(x, 7)
