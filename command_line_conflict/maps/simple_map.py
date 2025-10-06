from .base import Map


class SimpleMap(Map):
    """A simple, empty map with no walls.

    This map is a completely open area with no obstacles.
    """

    def __init__(self) -> None:
        super().__init__()
