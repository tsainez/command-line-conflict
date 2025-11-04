from .base import Map
from .. import factories
from ..components.environmental import Environmental
from ..components.light import Light

class MissionTwo(Map):
    """
    Mission Two: Nightfall

    This mission takes place at night with heavy fog of war. Units may equip a light modifier to slightly increase vision range, but it is otherwise severely reduced.
    """

    def __init__(self) -> None:
        """Initializes the MissionTwo map."""
        super().__init__(width=40, height=30)

    def initialize_entities(self, game_state) -> None:
        """Initializes the entities for the map."""
        # Add environmental settings
        environmental_id = game_state.create_entity()
        game_state.add_component(environmental_id, Environmental(is_day=False, fog_of_war=True))

        # Add some mineral patches
        factories.create_mineral_patch(game_state, 5, 5)
        factories.create_mineral_patch(game_state, 5, 6)
        factories.create_mineral_patch(game_state, 6, 5)
        factories.create_mineral_patch(game_state, 6, 6)

        factories.create_mineral_patch(game_state, 33, 23)
        factories.create_mineral_patch(game_state, 33, 24)
        factories.create_mineral_patch(game_state, 34, 23)
        factories.create_mineral_patch(game_state, 34, 24)

        # Add pre-placed enemy units with lights
        enemy1 = factories.create_chassis(game_state, 20, 15, player_id=2, is_human=False)
        game_state.add_component(enemy1, Light(radius=3))

        enemy2 = factories.create_chassis(game_state, 25, 20, player_id=2, is_human=False)
        game_state.add_component(enemy2, Light(radius=3))

        # Add buildings for both players
        player1_factory = factories.create_unit_factory(game_state, 5, 8, player_id=1, is_human=True)
        game_state.add_component(player1_factory, Light(radius=5))

        player2_factory = factories.create_unit_factory(game_state, 33, 26, player_id=2, is_human=False)
        game_state.add_component(player2_factory, Light(radius=5))
