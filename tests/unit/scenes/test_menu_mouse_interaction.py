import unittest
from unittest.mock import MagicMock

import pygame

from command_line_conflict.scenes.menu import MenuScene


class TestMenuMouse(unittest.TestCase):
    def setUp(self):
        self.mock_game = MagicMock()
        self.mock_game.screen.get_width.return_value = 800
        self.mock_game.font = MagicMock()
        self.mock_game.music_manager = MagicMock()

        # Initialize pygame font module since MenuScene creates fonts
        pygame.font.init()

        self.scene = MenuScene(self.mock_game)

    def test_mouse_hover_updates_selection(self):
        # Trigger a draw to populate rects (we don't care about the mock rects generated)
        surface_mock = MagicMock()
        self.scene.draw(surface_mock)

        # Replace mock rects with real rects to ensure collidepoint works as expected
        real_rects = [
            pygame.Rect(300, 300, 200, 50),  # Option 0
            pygame.Rect(300, 360, 200, 50),  # Option 1
            pygame.Rect(300, 420, 200, 50),  # Option 2
            pygame.Rect(300, 480, 200, 50),  # Option 3
        ]
        self.scene.option_rects = real_rects

        # Target index 1
        target_index = 1
        target_pos = real_rects[target_index].center

        event = MagicMock()
        event.type = pygame.MOUSEMOTION
        event.pos = target_pos

        self.scene.handle_event(event)

        # Check if selected option is now 1
        self.assertEqual(self.scene.selected_option, 1)

    def test_mouse_click_activates_option(self):
        # Trigger draw
        surface_mock = MagicMock()
        self.scene.draw(surface_mock)

        real_rects = [
            pygame.Rect(300, 300, 200, 50),  # Option 0
            pygame.Rect(300, 360, 200, 50),  # Option 1
            pygame.Rect(300, 420, 200, 50),  # Option 2
            pygame.Rect(300, 480, 200, 50),  # Option 3
        ]
        self.scene.option_rects = real_rects

        target_index = 3
        target_pos = real_rects[target_index].center

        # Hover first (to select it)
        move_event = MagicMock()
        move_event.type = pygame.MOUSEMOTION
        move_event.pos = target_pos
        self.scene.handle_event(move_event)

        self.assertEqual(self.scene.selected_option, target_index)

        # Click
        click_event = MagicMock()
        click_event.type = pygame.MOUSEBUTTONUP
        click_event.button = 1  # Left click
        click_event.pos = target_pos

        self.scene.handle_event(click_event)

        self.assertFalse(self.mock_game.running)

    def tearDown(self):
        pygame.font.quit()
