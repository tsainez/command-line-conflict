from dataclasses import dataclass

@dataclass
class Harvester:
    """A component that allows a unit to harvest minerals."""
    carrying: int = 0
    capacity: int = 10
