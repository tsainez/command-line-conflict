from .base import Map


class SimpleMap(Map):
    """A simple, empty map with no walls."""

    def __init__(self) -> None:
        """Initializes the SimpleMap."""
        super().__init__()
