from typing import List

from ..units import Unit


class Map:
    """Container for units present in a level."""

    def __init__(self) -> None:
        self.units: List[Unit] = []

    def spawn_unit(self, unit: Unit) -> None:
        self.units.append(unit)

    def update(self, dt: float) -> None:
        for u in list(self.units):
            u.update(dt)
