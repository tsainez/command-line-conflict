from .base import Component


class Position(Component):
    """A component that gives an entity a position in the world."""

    def __init__(self, x: float, y: float):
        """Initializes the Position component.

        Args:
            x: The x-coordinate of the entity.
            y: The y-coordinate of the entity.
        """
        self.x = x
        self.y = y
