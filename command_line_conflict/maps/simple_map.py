from .base import Map


class SimpleMap(Map):
    """Default map that is initially empty."""

    def __init__(self) -> None:
        super().__init__()
