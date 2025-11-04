from .base import Map
from .. import factories
from ..components.environmental import Environmental
from ..components.light import Light

class MissionThree(Map):
    """
    Mission Three: Dead of Night

    This mission takes place at night with no fog. So, if units have lights equipped then the bonus they receive is far greater— giving them something almost equivalent to daylight (but slightly inferior).
    """

    def __init__(self) -> None:
        """Initializes the MissionThree map."""
        super().__init__(width=50, height=40)

    def initialize_entities(self, game_state) -> None:
        """Initializes the entities for the map."""
        # Add environmental settings
        environmental_id = game_state.create_entity()
        game_state.add_component(environmental_id, Environmental(is_day=False, fog_of_war=False))

        # Add some mineral patches
        factories.create_mineral_patch(game_state, 5, 5)
        factories.create_mineral_patch(game_state, 5, 6)
        factories.create_mineral_patch(game_state, 6, 5)
        factories.create_mineral_patch(game_state, 6, 6)

        factories.create_mineral_patch(game_state, 43, 33)
        factories.create_mineral_patch(game_state, 43, 34)
        factories.create_mineral_patch(game_state, 44, 33)
        factories.create_mineral_patch(game_state, 44, 34)

        # Add pre-placed enemy units with lights
        enemy1 = factories.create_chassis(game_state, 20, 15, player_id=2, is_human=False)
        game_state.add_component(enemy1, Light(radius=10))

        enemy2 = factories.create_chassis(game_state, 25, 20, player_id=2, is_human=False)
        game_state.add_component(enemy2, Light(radius=10))

        enemy3 = factories.create_rover(game_state, 30, 25, player_id=2, is_human=False)
        game_state.add_component(enemy3, Light(radius=15))

        # Add buildings for both players
        player1_factory = factories.create_unit_factory(game_state, 5, 8, player_id=1, is_human=True)
        game_state.add_component(player1_factory, Light(radius=20))

        player2_factory = factories.create_unit_factory(game_state, 43, 36, player_id=2, is_human=False)
        game_state.add_component(player2_factory, Light(radius=20))
