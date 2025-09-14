from dataclasses import dataclass

@dataclass
class Owner:
    """Component that assigns ownership of an entity to a player."""
    player_id: int
