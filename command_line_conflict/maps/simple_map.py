from ..units import Airplane, Marine, Tank
from .base import Map


class SimpleMap(Map):
    """Default map with a few units."""

    def __init__(self) -> None:
        super().__init__()
        self.spawn_unit(Marine(5, 5))
        self.spawn_unit(Tank(10, 10))
        self.spawn_unit(Airplane(15, 5))
