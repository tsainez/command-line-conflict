from .base import Component


class Vision(Component):
    """
    A component that gives an entity vision.
    """

    def __init__(self, vision_range: int):
        self.vision_range = vision_range
