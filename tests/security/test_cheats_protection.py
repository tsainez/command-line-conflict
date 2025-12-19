from unittest.mock import MagicMock, patch

import pygame

from command_line_conflict.scenes.game import GameScene


class MockGame:
    def __init__(self):
        self.screen = MagicMock()
        self.font = MagicMock()
        self.music_manager = MagicMock()
        self.screen.get_size.return_value = (800, 600)
        self.scene_manager = MagicMock()
        self.steam = MagicMock()


def test_cheats_disabled_when_debug_false():
    """Verify that cheats are disabled when DEBUG is False."""
    with patch("command_line_conflict.config.DEBUG", False):
        game = MockGame()
        scene = GameScene(game)

        # Initial state
        assert scene.cheats["reveal_map"] is False
        assert scene.cheats["god_mode"] is False

        # Simulate F1 (Reveal Map)
        event = MagicMock()
        event.type = pygame.KEYDOWN
        event.key = pygame.K_F1
        scene.handle_event(event)

        # This assertion should fail before the fix
        assert scene.cheats["reveal_map"] is False, "Reveal Map cheat should not toggle when DEBUG is False"

        # Simulate F2 (God Mode)
        event.key = pygame.K_F2
        scene.handle_event(event)

        # This assertion should fail before the fix
        assert scene.cheats["god_mode"] is False, "God Mode cheat should not toggle when DEBUG is False"


def test_cheats_enabled_when_debug_true():
    """Verify that cheats work when DEBUG is True."""
    with patch("command_line_conflict.config.DEBUG", True):
        game = MockGame()
        scene = GameScene(game)

        # Simulate F1
        event = MagicMock()
        event.type = pygame.KEYDOWN
        event.key = pygame.K_F1
        scene.handle_event(event)

        assert scene.cheats["reveal_map"] is True, "Reveal Map cheat should toggle when DEBUG is True"
