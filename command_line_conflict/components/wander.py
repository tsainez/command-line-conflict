from .base import Component


class Wander(Component):
    """A component that causes an entity to wander randomly."""

    def __init__(self, wander_radius: int = 5, move_interval: float = 3.0):
        """Initializes the Wander component.

        Args:
            wander_radius: The maximum distance to wander from the current position.
            move_interval: The time in seconds to wait between moves.
        """
        self.wander_radius = wander_radius
        self.move_interval = move_interval
        self.time_since_last_move = 0.0
