import pytest
from unittest.mock import MagicMock, patch
import pygame
from command_line_conflict.scenes.menu import MenuScene

class TestMenuUXQuit:

    @pytest.fixture
    def mock_game(self):
        game = MagicMock()
        game.screen.get_width.return_value = 800
        game.screen.get_height.return_value = 600
        game.music_manager = MagicMock()
        game.running = True
        return game

    def test_quit_requires_confirmation(self, mock_game):
        """Test that clicking Quit once does not quit immediately but asks for confirmation."""
        with patch("pygame.font.Font"), patch("command_line_conflict.scenes.menu.CampaignManager"):
            menu = MenuScene(mock_game)

            # Find index of "Quit"
            quit_index = menu.menu_options.index("Quit")

            # First click
            menu._trigger_option(quit_index)

            # Should NOT have quit yet
            assert mock_game.running is True
            # Should be in confirmation state (we'll check public attribute or behavior)
            # Since implementation isn't done, we expect this to fail if it was immediately quitting
            # But currently it immediately quits, so this assertion will fail.

    def test_quit_confirmation_behavior(self, mock_game):
        """Test the full flow: Click -> Confirm -> Quit."""
        with patch("pygame.font.Font"), patch("command_line_conflict.scenes.menu.CampaignManager"):
            menu = MenuScene(mock_game)
            quit_index = menu.menu_options.index("Quit")

            # First click: Activate confirmation
            menu._trigger_option(quit_index)
            assert mock_game.running is True
            assert getattr(menu, "confirm_quit", False) is True

            # Second click: Confirm quit
            menu._trigger_option(quit_index)
            assert mock_game.running is False

    def test_quit_confirmation_reset_on_navigation(self, mock_game):
        """Test that navigating away resets the confirmation state."""
        with patch("pygame.font.Font"), patch("command_line_conflict.scenes.menu.CampaignManager"):
            menu = MenuScene(mock_game)
            quit_index = menu.menu_options.index("Quit")

            # Activate confirmation
            menu._trigger_option(quit_index)
            assert getattr(menu, "confirm_quit", False) is True

            # Simulate navigating up
            event = MagicMock()
            event.type = pygame.KEYDOWN
            event.key = pygame.K_UP
            menu.handle_event(event)

            assert getattr(menu, "confirm_quit", False) is False

    def test_quit_confirmation_reset_on_hover(self, mock_game):
        """Test that hovering another option resets confirmation."""
        with patch("pygame.font.Font"), patch("command_line_conflict.scenes.menu.CampaignManager"):
            menu = MenuScene(mock_game)
            quit_index = menu.menu_options.index("Quit")

            # Activate confirmation
            menu._trigger_option(quit_index)

            # Simulate hovering another option
            # We need to setup option_rects for this to work
            other_index = (quit_index - 1)
            menu.option_rects = [
                (pygame.Rect(0, 0, 100, 20), other_index),
                (pygame.Rect(0, 50, 100, 20), quit_index)
            ]

            event = MagicMock()
            event.type = pygame.MOUSEMOTION
            event.pos = (10, 10) # Hits first rect (other_index)

            menu.handle_event(event)

            assert getattr(menu, "confirm_quit", False) is False
