from .base import Component


class Renderable(Component):
    """Allows an entity to be rendered on the screen.

    This component defines the visual representation of an entity, including its
    icon and color.

    Attributes:
        icon (str): The character used to represent the entity on the screen.
        color (tuple[int, int, int]): The RGB color of the entity's icon.
    """

    def __init__(self, icon: str, color: tuple[int, int, int] = (255, 255, 255)):
        """Initializes the Renderable component.

        Args:
            icon: The character used to represent the entity on the screen.
            color: The color of the entity.
        """
        self.icon = icon
        self.color = color
