from command_line_conflict.components.factory import Factory
from command_line_conflict.components.player import Player
from command_line_conflict.components.position import Position
from command_line_conflict.components.renderable import Renderable
from command_line_conflict.game_state import GameState
from command_line_conflict.maps.base import Map
from command_line_conflict.systems.factory_system import FactorySystem


class MockMap(Map):
    def __init__(self, width=50, height=50):
        super().__init__(width, height)

    def draw(self, screen, font, camera=None):
        pass


def test_factory_system_produces_unit():
    """Tests that the factory system correctly produces a unit."""
    game_state = GameState(MockMap())
    factory_system = FactorySystem()

    # Create a factory
    factory_id = game_state.create_entity()
    game_state.add_component(factory_id, Position(10, 10))
    game_state.add_component(factory_id, Player(player_id=1, is_human=True))
    game_state.add_component(
        factory_id, Factory(unit_types=["chassis"], production_time=5.0)
    )

    # Queue a unit for production
    factory = game_state.get_component(factory_id, Factory)
    factory.production_queue.append("chassis")

    # Simulate time passing
    factory_system.update(game_state, 5.0)

    # Check that the unit was created
    unit_found = False
    for entity_id, components in game_state.entities.items():
        if components.get(Renderable) and components.get(Renderable).icon == "C":
            unit_found = True
            unit_pos = components.get(Position)
            assert unit_pos.x == 10
            assert unit_pos.y == 12  # Spawns below factory
            break
    assert unit_found

    # Check that the production queue is empty
    assert not factory.production_queue