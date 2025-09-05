from .base import Component


class Position(Component):
    """A component that gives an entity a position in the world."""

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
