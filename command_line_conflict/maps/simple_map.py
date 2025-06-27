from .base import Map
from ..units import Unit, Airplane


class SimpleMap(Map):
    """Default map with a few units."""

    def __init__(self) -> None:
        super().__init__()
        self.spawn_unit(Unit(5, 5))
        self.spawn_unit(Unit(10, 10))
        self.spawn_unit(Airplane(15, 5))
