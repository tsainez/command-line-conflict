from command_line_conflict.components.builder import Builder
from command_line_conflict.components.player import Player
from command_line_conflict.components.position import Position
from command_line_conflict.components.renderable import Renderable
from command_line_conflict.game_state import GameState
from command_line_conflict.maps.base import Map
from command_line_conflict.systems.build_system import BuildSystem


class MockMap(Map):
    def __init__(self, width=50, height=50):
        super().__init__(width, height)

    def draw(self, screen, font, camera=None):
        pass


def test_build_system_creates_factory():
    """Tests that the build system correctly creates a factory."""
    game_state = GameState(MockMap())
    build_system = BuildSystem()

    # Create a builder unit
    builder_id = game_state.create_entity()
    game_state.add_component(builder_id, Position(10, 10))
    game_state.add_component(builder_id, Player(player_id=1, is_human=True))
    game_state.add_component(builder_id, Builder(build_types=["unit_factory"]))

    # Create a construction site
    site_id = game_state.create_entity()
    game_state.add_component(site_id, Position(10, 12))
    game_state.add_component(site_id, Renderable(icon="X"))

    # Set the builder's target
    builder = game_state.get_component(builder_id, Builder)
    builder.build_target = site_id

    # Simulate time passing
    build_system.update(game_state, 5.0)

    # Check that the factory was created
    factory_found = False
    for entity_id, components in game_state.entities.items():
        if components.get(Renderable) and components.get(Renderable).icon == "F":
            factory_found = True
            factory_pos = components.get(Position)
            assert factory_pos.x == 10
            assert factory_pos.y == 12
            break
    assert factory_found

    # Check that the construction site was removed
    assert site_id not in game_state.entities