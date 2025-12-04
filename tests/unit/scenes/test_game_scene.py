import pygame

from command_line_conflict.components.attack import Attack
from command_line_conflict.components.position import Position
from command_line_conflict.components.selectable import Selectable
from command_line_conflict.components.movable import Movable
from command_line_conflict.game_state import GameState
from command_line_conflict.maps.simple_map import SimpleMap
from command_line_conflict.scenes.game import GameScene


class MockGame:
    def __init__(self):
        self.screen = None
        self.font = None


def test_move_command_interrupts_attack():
    # Arrange
    game = MockGame()
    game_scene = GameScene(game)
    game_state = game_scene.game_state

    attacker_id = game_state.create_entity()
    game_state.add_component(attacker_id, Position(0, 0))
    game_state.add_component(attacker_id, Attack(attack_damage=10, attack_range=5, attack_speed=1.0))
    game_state.add_component(attacker_id, Selectable())
    game_state.entities[attacker_id][Selectable].is_selected = True

    target_id = game_state.create_entity()
    game_state.add_component(target_id, Position(3, 3))
    game_state.entities[attacker_id][Attack].attack_target = target_id

    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 3, "pos": (100, 100)})

    # Act
    game_scene.handle_event(event)

    # Assert
    assert game_state.entities[attacker_id][Attack].attack_target is None

def test_patrol_command_flow():
    game = MockGame()
    game_scene = GameScene(game)
    game_state = game_scene.game_state

    # Create selectable unit
    unit_id = game_state.create_entity()
    game_state.add_component(unit_id, Position(10, 10))
    game_state.add_component(unit_id, Selectable())
    game_state.add_component(unit_id, Movable(speed=1.0))
    game_state.entities[unit_id][Selectable].is_selected = True

    # Press 'P' to enter patrol mode
    event_p = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_p})
    game_scene.handle_event(event_p)

    assert game_scene.command_mode == "PATROL"

    # Left click to issue command
    # pos (200, 200) -> grid roughly (10, 10) depending on camera/zoom
    # Default camera zoom 1.0. Grid size 20.
    # 200 / 20 = 10. So clicking at 10,10 relative to camera.
    # Camera defaults to 0,0? Let's check Camera init.
    # Assuming camera is at 0,0.
    # Let's click at 300, 300 -> 15, 15
    event_click = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": (300, 300)})
    game_scene.handle_event(event_click)

    assert game_scene.command_mode == "NONE"

    movable = game_state.get_component(unit_id, Movable)
    assert movable.is_patrolling
    assert movable.patrol_end == (15, 15)

def test_pause_command_flow():
    game = MockGame()
    game_scene = GameScene(game)

    assert not game_scene.paused

    # Press SPACE to pause
    event_space = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_SPACE})
    game_scene.handle_event(event_space)

    assert game_scene.paused

    # Press SPACE to unpause
    game_scene.handle_event(event_space)

    assert not game_scene.paused

    # Ensure 'P' no longer pauses
    event_p = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_p})
    game_scene.handle_event(event_p)
    assert not game_scene.paused # P should not pause
