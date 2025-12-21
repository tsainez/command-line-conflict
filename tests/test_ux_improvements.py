from unittest.mock import MagicMock

import pygame

from command_line_conflict.camera import Camera
from command_line_conflict.scenes.game import GameScene
from command_line_conflict.systems.ui_system import UISystem


class MockGame:
    def __init__(self):
        self.screen = MagicMock()
        self.font = MagicMock()
        self.music_manager = MagicMock()
        self.scene_manager = MagicMock()


def test_ui_system_help_text_content():
    screen = MagicMock()
    font = MagicMock()
    camera = Camera()
    ui = UISystem(screen, font, camera)

    # This is what we WANT.
    expected_options = [
        "L-Click: Select",
        "R-Click: Move",
        "H: Hold Position",
        "P / Space: Pause",
        "Cam: Arrows / Drag",
        "ESC: Menu",
    ]

    # We allow some variation but key elements must be present
    assert ui.key_options == expected_options


def test_game_scene_space_pause():
    game = MockGame()
    scene = GameScene(game)
    scene.paused = False

    # Create a Space KeyDown event
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)
    scene.handle_event(event)

    assert scene.paused is True, "Spacebar did not toggle pause"

    scene.handle_event(event)
    assert scene.paused is False, "Spacebar did not toggle pause back"
