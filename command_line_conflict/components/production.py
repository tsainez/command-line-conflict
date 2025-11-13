from dataclasses import dataclass, field
from typing import List

@dataclass
class Production:
    """A component that allows a building to produce units."""
    queue: List[str] = field(default_factory=list)
    progress: float = 0.0
    time_to_produce: float = 5.0  # seconds
