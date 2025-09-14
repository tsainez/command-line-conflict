from .base import Component


class Player(Component):
    """A component that identifies an entity as belonging to a player."""

    def __init__(self, player_id: int):
        """Initializes the Player component.

        Args:
            player_id: The ID of the player.
        """
        self.player_id = player_id
