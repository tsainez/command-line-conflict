from .base import Map
from .. import factories


class SimpleMap(Map):
    """A simple, empty map with no walls."""

    def __init__(self) -> None:
        """Initializes the SimpleMap."""
        super().__init__()

    def initialize_entities(self, game_state) -> None:
        """Creates the starting units for each player."""
        # Player 1 units (human)
        for i in range(3):
            factories.create_chassis(
                game_state, 10 + i * 2, 10, player_id=1, is_human=True
            )
        # Player 2 units (AI)
        for i in range(3):
            factories.create_chassis(
                game_state, 40 + i * 2, 40, player_id=2, is_human=False
            )
