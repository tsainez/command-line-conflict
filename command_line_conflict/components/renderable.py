from .base import Component


class Renderable(Component):
    """A component that makes an entity renderable on the screen."""

    def __init__(
        self,
        icon: str,
        color: tuple[int, int, int] = (255, 255, 255),
        size: float = 0.5,
    ):
        """Initializes the Renderable component.

        Args:
            icon: The character used to represent the entity on the screen.
            color: The color of the entity.
            size: The radius of the entity, used for collision detection.
        """
        self.icon = icon
        self.color = color
        self.size = size
