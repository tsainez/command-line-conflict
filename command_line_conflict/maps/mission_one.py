from .base import Map
from .. import factories
from ..components.environmental import Environmental

class MissionOne(Map):
    """
    Mission One: Broad Daylight

    This mission takes place in broad daylight. There is no fog of war and no vision modifiers.
    """

    def __init__(self) -> None:
        """Initializes the MissionOne map."""
        super().__init__(width=30, height=20)

    def initialize_entities(self, game_state) -> None:
        """Initializes the entities for the map."""
        # Add environmental settings
        environmental_id = game_state.create_entity()
        game_state.add_component(environmental_id, Environmental(is_day=True, fog_of_war=False))

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

        # Add buildings for both players
        factories.create_unit_factory(game_state, 5, 8, player_id=1, is_human=True)
        factories.create_unit_factory(game_state, 23, 16, player_id=2, is_human=False)
