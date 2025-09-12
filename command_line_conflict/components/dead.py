from .base import Component


class Dead(Component):
    """
    A component that marks an entity as dead.
    """

    def __init__(self, timer: float = 0.0):
        self.timer = timer
