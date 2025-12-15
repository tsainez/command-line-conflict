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
