import os
import pygame
import pytest
from unittest.mock import MagicMock, patch
from command_line_conflict import config
from command_line_conflict.scenes.settings import SettingsScene
from command_line_conflict.engine import Game

@pytest.fixture
def mock_game():
    game = MagicMock()
    game.screen = MagicMock()
    game.scene_manager = MagicMock()
    return game

def test_settings_fullscreen_toggle(mock_game):
    # Initialize pygame for constants
    pygame.init()

    # Reset config
    config.FULLSCREEN = False

    scene = SettingsScene(mock_game)

    # Option 1 is Fullscreen (0 is Screen Size)
    scene.selected_option = 1

    # Mock pygame.display.set_mode
    with patch("pygame.display.set_mode") as mock_set_mode:
        # Simulate Enter key press to toggle ON
        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)
        scene.handle_event(event)

        assert config.FULLSCREEN is True
        mock_set_mode.assert_called_with((config.SCREEN["width"], config.SCREEN["height"]), pygame.FULLSCREEN)

        # Simulate Enter key press to toggle OFF
        scene.handle_event(event)

        assert config.FULLSCREEN is False
        mock_set_mode.assert_called_with((config.SCREEN["width"], config.SCREEN["height"]), 0)

def test_settings_screen_size_preserves_fullscreen(mock_game):
    # Initialize pygame
    pygame.init()

    # Set fullscreen to True
    config.FULLSCREEN = True

    scene = SettingsScene(mock_game)

    # Option 0 is Screen Size
    scene.selected_option = 0

    # Mock pygame.display.set_mode
    with patch("pygame.display.set_mode") as mock_set_mode:
        # Simulate Enter key press to change resolution
        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)
        scene.handle_event(event)

        # Check that pygame.FULLSCREEN was passed
        mock_set_mode.assert_called()
        args, kwargs = mock_set_mode.call_args
        flags = args[1]
        assert flags == pygame.FULLSCREEN

if __name__ == "__main__":
    # Manually run if executed as script
    pass
