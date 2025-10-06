from .base import Component


class Movable(Component):
    """Allows an entity to move across the game map.

    This component stores information about an entity's movement capabilities,
    current destination, and path.

    Attributes:
        speed (float): The movement speed of the entity in tiles per second.
        target_x (float | None): The x-coordinate of the entity's destination.
        target_y (float | None): The y-coordinate of the entity's destination.
        path (list[tuple[int, int]]): A list of (x, y) tuples representing the
            path the entity is currently following.
        can_fly (bool): If True, the entity can move over obstacles.
        intelligent (bool): If True, the entity uses pathfinding to navigate
            around other units.
    """

    def __init__(self, speed: float, can_fly: bool = False, intelligent: bool = True):
        """Initializes the Movable component.

        Args:
            speed: The speed at which the entity moves.
            can_fly: Whether the entity can fly over obstacles.
            intelligent: Whether the entity uses intelligent pathfinding to
                         avoid other units.
        """
        self.speed = speed
        self.target_x: float | None = None
        self.target_y: float | None = None
        self.path: list[tuple[int, int]] = []
        self.can_fly = can_fly
        self.intelligent = intelligent
