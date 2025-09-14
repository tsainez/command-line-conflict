from dataclasses import dataclass, field
from typing import List, Any

from .base import Component

@dataclass
class Production(Component):
    production_queue: list[Any] = field(default_factory=list)
    progress: float = 0.0
