from .base import Component


class Selectable(Component):
    """A component that makes an entity selectable by the player."""

    def __init__(self) -> None:
        """Initializes the Selectable component."""
        self.is_selected = False
