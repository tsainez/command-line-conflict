from dataclasses import dataclass

@dataclass
class Light:
    """A component that increases a unit's vision range at night."""
    radius: int
