from .base import Component


class Selectable(Component):
    """Marks an entity as selectable by the player.

    Attributes:
        is_selected (bool): A flag indicating whether the entity is currently
            selected by the player.
    """

    def __init__(self):
        self.is_selected = False
