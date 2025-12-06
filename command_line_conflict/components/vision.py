from .base import Component


class Vision(Component):
    """A component that gives an entity vision."""

    def __init__(self, vision_range: int) -> None:
        """Initializes the Vision component.

        Args:
            vision_range: The maximum distance the entity can see.
        """
        self.vision_range = vision_range
