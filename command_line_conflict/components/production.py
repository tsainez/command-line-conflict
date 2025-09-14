from dataclasses import dataclass, field
from typing import List

@dataclass
class Production:
    """Component for units that can produce other units."""
    production_list: List[str] = field(default_factory=list)
