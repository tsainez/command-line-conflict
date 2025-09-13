from dataclasses import dataclass


@dataclass
class Player:
    """
    Component that identifies a unit as belonging to a player.
    """

    player_id: int
