from .base import Component


class Dead(Component):
    """Marks an entity as dead and schedules it for removal.

    Attributes:
        timer (float): The time in seconds remaining before the entity's corpse
            is removed from the game.
    """

    def __init__(self, timer: float = 0.0):
        """Initializes the Dead component.

        Args:
            timer: The time in seconds before the entity's corpse is removed.
        """
        self.timer = timer
