from .base import Component


class Player(Component):
    """A component that identifies an entity as belonging to a player."""

    def __init__(self, player_id: int, is_human: bool = False) -> None:
        """Initializes the Player component.

        Args:
            player_id: The ID of the player.
            is_human: True if the player is human-controlled.
        """
        self.player_id = player_id
        self.is_human = is_human
