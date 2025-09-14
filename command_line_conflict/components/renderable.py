from .base import Component


class Renderable(Component):
    """A component that makes an entity renderable on the screen."""

    def __init__(self, icon: str, color: tuple[int, int, int] = (255, 255, 255)):
        """Initializes the Renderable component.

        Args:
            icon: The character used to represent the entity on the screen.
            color: The color of the entity.
        """
        self.icon = icon
        self.color = color
