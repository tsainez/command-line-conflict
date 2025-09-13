from .base import Component


class Renderable(Component):
    """A component that makes an entity renderable on the screen."""

    def __init__(self, icon: str):
        """Initializes the Renderable component.

        Args:
            icon: The character used to represent the entity on the screen.
        """
        self.icon = icon
