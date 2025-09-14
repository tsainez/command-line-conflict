import pygame
from command_line_conflict import factories
from command_line_conflict.scenes.game import GameScene
from command_line_conflict.components.selectable import Selectable
from command_line_conflict.components.harvester import Harvester
from command_line_conflict.components.factory import Factory
from command_line_conflict.components.production import Production
from command_line_conflict.components.position import Position
from command_line_conflict.components.renderable import Renderable

def test_factory_creation_and_production(game_state):
    # 1. Create a harvester
    harvester_id = factories.create_extractor(game_state, 5, 5)
    assert game_state.get_component(harvester_id, Harvester) is not None

    # 2. Select the harvester
    game_state.get_component(harvester_id, Selectable).is_selected = True

    # 3. Simulate pressing 'b' to build a factory
    game = type('Game', (), {'font': None, 'scene_manager': None, 'screen': None})()
    game_scene = GameScene(game)
    game_scene.game_state = game_state
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_b)
    game_scene.handle_event(event)

    # 4. Check if a factory is created
    factory_id = -1
    for entity_id, components in game_state.entities.items():
        if components.get(Factory):
            factory_id = entity_id
            break

    assert factory_id != -1
    assert game_state.get_component(factory_id, Factory) is not None
    production = game_state.get_component(factory_id, Production)
    assert production is not None
    assert production.production_list == ["Chassis", "Rover"]

    # 5. Deselect harvester and select factory
    game_state.get_component(harvester_id, Selectable).is_selected = False
    game_state.get_component(factory_id, Selectable).is_selected = True

    # 6. Simulate pressing '1' to produce a chassis
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_1)
    game_scene.handle_event(event)

    # 7. Check if a chassis is created
    chassis_id = -1
    for entity_id, components in game_state.entities.items():
        renderable = components.get(Renderable)
        if renderable and renderable.icon == "C":
            chassis_id = entity_id
            break

    assert chassis_id != -1
