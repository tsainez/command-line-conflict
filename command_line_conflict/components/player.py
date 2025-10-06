from .base import Component


class Player(Component):
    """Identifies an entity as belonging to a specific player.

    This component is used to associate entities with a player, distinguishing
    between human and AI-controlled players.

    Attributes:
        player_id (int): The unique identifier for the player.
        is_human (bool): If True, this entity is controlled by a human player.
    """

    def __init__(self, player_id: int, is_human: bool = False):
        """Initializes the Player component.

        Args:
            player_id: The ID of the player.
            is_human: True if the player is human-controlled.
        """
        self.player_id = player_id
        self.is_human = is_human
