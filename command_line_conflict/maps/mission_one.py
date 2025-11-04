from .base import Map
from .. import factories

class MissionOne(Map):
    """The first mission of the campaign."""

    def __init__(self) -> None:
        """Initializes the MissionOne map."""
        super().__init__(width=30, height=20)

    def initialize_entities(self, game_state) -> None:
        """Initializes the entities for the map."""
        # Add some mineral patches
        factories.create_mineral_patch(game_state, 5, 5)
        factories.create_mineral_patch(game_state, 5, 6)
        factories.create_mineral_patch(game_state, 6, 5)
        factories.create_mineral_patch(game_state, 6, 6)

        factories.create_mineral_patch(game_state, 23, 13)
        factories.create_mineral_patch(game_state, 23, 14)
        factories.create_mineral_patch(game_state, 24, 13)
        factories.create_mineral_patch(game_state, 24, 14)

        # Add a pre-placed enemy unit
        factories.create_chassis(game_state, 20, 10, player_id=2, is_human=False)
