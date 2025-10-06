from .base import Component


class Position(Component):
    """Stores the position of an entity on the game map.

    Attributes:
        x (float): The x-coordinate of the entity.
        y (float): The y-coordinate of the entity.
    """

    def __init__(self, x: float, y: float):
        """Initializes the Position component.

        Args:
            x: The x-coordinate of the entity.
            y: The y-coordinate of the entity.
        """
        self.x = x
        self.y = y
