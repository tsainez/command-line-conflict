from .base import Component


class Movable(Component):
    """A component that allows an entity to move."""

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
        self.hold_position: bool = False

        # Optimization: Throttling for pathfinding failures
        self.path_retry_timer: float = 0.0
