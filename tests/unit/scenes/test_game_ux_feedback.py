from unittest.mock import MagicMock

import pygame

from command_line_conflict import config
from command_line_conflict.scenes.game import GameScene


class MockGame:
    def __init__(self):
        self.screen = MagicMock()
        self.font = MagicMock()
        self.music_manager = MagicMock()
        # Mock screen get_size for grid drawing logic
        self.screen.get_size.return_value = (800, 600)
        self.running = True


def test_hold_position_feedback(mocker):
    """Verifies that the Hold Position command gives visual feedback via chat."""
    # Arrange
    mocker.patch("command_line_conflict.config.DEBUG", True)
    mock_logger = mocker.patch("command_line_conflict.scenes.game.log")

    game = MockGame()
    scene = GameScene(game)
    scene.chat_system = MagicMock()
    scene.chat_system.handle_event.return_value = False  # Important: Chat shouldn't consume event

    # Simulate 'H' key press
    event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_h, "mod": 0})

    # Act
    scene.handle_event(event)

    # Assert
    scene.chat_system.add_message.assert_called_with("Hold Position command issued", (255, 255, 0))


def test_cheat_reveal_map_feedback(mocker):
    """Verifies that the Reveal Map cheat gives visual feedback."""
    # Arrange
    mocker.patch("command_line_conflict.config.DEBUG", True)

    game = MockGame()
    scene = GameScene(game)
    scene.chat_system = MagicMock()
    scene.chat_system.handle_event.return_value = False

    # Simulate 'F1' key press
    event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_F1, "mod": 0})

    # Act
    scene.handle_event(event)

    # Assert
    scene.chat_system.add_message.assert_called()
    assert "Map Reveal" in scene.chat_system.add_message.call_args[0][0]


def test_cheat_god_mode_feedback(mocker):
    """Verifies that the God Mode cheat gives visual feedback."""
    # Arrange
    mocker.patch("command_line_conflict.config.DEBUG", True)

    game = MockGame()
    scene = GameScene(game)
    scene.chat_system = MagicMock()
    scene.chat_system.handle_event.return_value = False

    # Simulate 'F2' key press
    event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_F2, "mod": 0})

    # Act
    scene.handle_event(event)

    # Assert
    scene.chat_system.add_message.assert_called()
    assert "God Mode" in scene.chat_system.add_message.call_args[0][0]


def test_cheat_switch_player_feedback(mocker):
    """Verifies that Switching Player gives visual feedback."""
    # Arrange
    mocker.patch("command_line_conflict.config.DEBUG", True)

    game = MockGame()
    scene = GameScene(game)
    scene.chat_system = MagicMock()
    scene.chat_system.handle_event.return_value = False

    # Simulate 'TAB' key press
    event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_TAB, "mod": 0})

    # Act
    scene.handle_event(event)

    # Assert
    scene.chat_system.add_message.assert_called()
    assert "Switched to player" in scene.chat_system.add_message.call_args[0][0]
