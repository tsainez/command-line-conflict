from .base import Component


class Renderable(Component):
    """A component that makes an entity renderable on the screen."""

    def __init__(self, icon: str):
        self.icon = icon
