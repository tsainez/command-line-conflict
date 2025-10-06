from .base import Component


class Vision(Component):
    """Gives an entity a line of sight.

    This component defines the range at which an entity can "see" the game
    world, which is used for revealing the fog of war.

    Attributes:
        vision_range (int): The maximum distance, in tiles, that the entity can see.
    """

    def __init__(self, vision_range: int):
        """Initializes the Vision component.

        Args:
            vision_range: The maximum distance the entity can see.
        """
        self.vision_range = vision_range
