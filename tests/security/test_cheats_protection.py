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


def test_tab_cheat_disabled_when_debug_false():
    """Verify that the TAB team switch cheat is disabled when DEBUG is False."""
    with patch("command_line_conflict.config.DEBUG", False):
        game = MockGame()
        scene = GameScene(game)

        initial_player_id = scene.current_player_id

        event = MagicMock()
        event.type = pygame.KEYDOWN
        event.key = pygame.K_TAB
        scene.handle_event(event)

        assert scene.current_player_id == initial_player_id, "TAB cheat should not change player when DEBUG is False"


def test_chat_log_toggle_disabled_when_dev_mode_false():
    """Verify that the chat log toggle (L key) is disabled when DEV_MODE is False."""
    from command_line_conflict.systems.chat_system import ChatSystem

    with patch("command_line_conflict.config.DEV_MODE", False):
        screen = MagicMock()
        font = MagicMock()
        chat = ChatSystem(screen, font)

        initial_show_log = chat.show_log

        event = MagicMock()
        event.type = pygame.KEYDOWN
        event.key = pygame.K_l
        chat.handle_event(event)

        assert chat.show_log == initial_show_log, "L key should not toggle chat log when DEV_MODE is False"


def test_chat_log_toggle_enabled_when_dev_mode_true():
    """Verify that the chat log toggle (L key) works when DEV_MODE is True."""
    from command_line_conflict.systems.chat_system import ChatSystem

    with patch("command_line_conflict.config.DEV_MODE", True):
        screen = MagicMock()
        font = MagicMock()
        chat = ChatSystem(screen, font)

        initial_show_log = chat.show_log

        event = MagicMock()
        event.type = pygame.KEYDOWN
        event.key = pygame.K_l
        chat.handle_event(event)

        assert chat.show_log != initial_show_log, "L key should toggle chat log when DEV_MODE is True"
