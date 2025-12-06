from .base import Component


class Dead(Component):
    """A component that marks an entity as dead."""

    def __init__(self, timer: float = 0.0) -> None:
        """Initializes the Dead component.

        Args:
            timer: The time in seconds before the entity's corpse is removed.
        """
        self.timer = timer
