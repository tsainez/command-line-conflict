import pygame
from command_line_conflict import factories
from command_line_conflict.scenes.game import GameScene
from command_line_conflict.components.selectable import Selectable
from command_line_conflict.components.harvester import Harvester
from command_line_conflict.components.factory import Factory
from command_line_conflict.components.production import Production
from command_line_conflict.components.position import Position
from command_line_conflict.components.renderable import Renderable
from command_line_conflict.components.owner import Owner

def test_factory_creation_and_production_with_player_system(game_state):
    # 1. Mock the player system
    game_state.players = {
        1: type('Player', (), {'id': 1, 'resources': 1000, 'color': (255, 0, 0)})(),
        2: type('Player', (), {'id': 2, 'resources': 1000, 'color': (0, 0, 255)})()
    }
    game_state.current_player_id = 1

    # 2. Create a harvester for player 1
    harvester_id = factories.create_extractor(game_state, 5, 5, 1)
    assert game_state.get_component(harvester_id, Harvester) is not None
    assert game_state.get_component(harvester_id, Owner).player_id == 1

    # 3. Select the harvester
    game_state.get_component(harvester_id, Selectable).is_selected = True

    # 4. Simulate pressing 'b' to build a factory
    game = type('Game', (), {'font': None, 'scene_manager': None, 'screen': None})()
    game_scene = GameScene(game)
    game_scene.game_state = game_state
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_b)
    game_scene.handle_event(event)

    # 5. Check if a factory is created and owned by player 1
    factory_id = -1
    for entity_id, components in game_state.entities.items():
        if components.get(Factory):
            factory_id = entity_id
            break

    assert factory_id != -1
    assert game_state.get_component(factory_id, Owner).player_id == 1

    # 6. Deselect harvester and select factory
    game_state.get_component(harvester_id, Selectable).is_selected = False
    game_state.get_component(factory_id, Selectable).is_selected = True

    # 7. Simulate pressing '1' to produce a chassis
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_1)
    game_scene.handle_event(event)

    # 8. Check if a chassis is created and owned by player 1
    chassis_id = -1
    for entity_id, components in game_state.entities.items():
        renderable = components.get(Renderable)
        if renderable and renderable.icon == "C":
            chassis_id = entity_id
            break

    assert chassis_id != -1
    assert game_state.get_component(chassis_id, Owner).player_id == 1
