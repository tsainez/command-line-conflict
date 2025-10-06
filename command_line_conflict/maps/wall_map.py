from .base import Map


class WallMap(Map):
    """A map featuring a horizontal wall with a single gap.

    This map is designed to test pathfinding around obstacles. It creates a
    horizontal wall across the center of the map, with a small opening
    to allow units to pass through.
    """

    def __init__(self) -> None:
        super().__init__(width=20, height=15)

        # Create a simple horizontal wall with a gap
        for x in range(3, 17):
            if x != 10:
                self.add_wall(x, 7)
