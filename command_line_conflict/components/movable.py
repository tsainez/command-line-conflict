from .base import Component


class Movable(Component):
    """A component that allows an entity to move."""

    def __init__(self, speed: float, can_fly: bool = False):
        self.speed = speed
        self.target_x: float | None = None
        self.target_y: float | None = None
        self.path: list[tuple[int, int]] = []
        self.can_fly = can_fly
