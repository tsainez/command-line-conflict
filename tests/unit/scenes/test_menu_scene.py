import unittest
from unittest.mock import MagicMock

import pygame

from command_line_conflict.scenes.menu import MenuScene


class TestMenuScene(unittest.TestCase):
    def setUp(self):
        self.mock_game = MagicMock()
        self.mock_game.font = MagicMock()
        # Mock music manager
        self.mock_game.music_manager = MagicMock()
        self.scene = MenuScene(self.mock_game)

    def test_menu_options(self):
        self.assertIn("Map Editor", self.scene.menu_options)

    def test_switch_to_editor(self):
        # Select "Map Editor" (index 1)
        self.scene.selected_option = 1

        event = MagicMock()
        event.type = pygame.KEYDOWN
        event.key = pygame.K_RETURN

        self.scene.handle_event(event)

        self.mock_game.scene_manager.switch_to.assert_called_with("editor")

    def test_mouse_hover_selects_option(self):
        # Setup mock rects
        mock_rect_0 = MagicMock()
        mock_rect_0.collidepoint.return_value = False
        mock_rect_1 = MagicMock()
        mock_rect_1.collidepoint.return_value = True  # Simulate hover over option 1

        self.scene.option_rects = [(mock_rect_0, 0), (mock_rect_1, 1)]

        event = MagicMock()
        event.type = pygame.MOUSEMOTION
        event.pos = (100, 100)

        self.scene.handle_event(event)

        self.assertEqual(self.scene.selected_option, 1)

    def test_mouse_click_triggers_option(self):
        # Setup mock rects
        mock_rect_0 = MagicMock()
        mock_rect_0.collidepoint.return_value = False
        mock_rect_1 = MagicMock()
        mock_rect_1.collidepoint.return_value = True  # Simulate click on option 1

        self.scene.option_rects = [(mock_rect_0, 0), (mock_rect_1, 1)]

        event = MagicMock()
        event.type = pygame.MOUSEBUTTONUP
        event.pos = (100, 100)

        self.scene.handle_event(event)

        self.mock_game.scene_manager.switch_to.assert_called_with("editor")
