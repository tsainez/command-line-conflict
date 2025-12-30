# pylint: disable=no-member
import unittest
from unittest.mock import MagicMock, patch

import pygame

from command_line_conflict.scenes.menu import MenuScene

# Patch SoundSystem before importing MenuScene if it was imported at module level,
# but since it's imported inside the module, we need to patch it where it is used.
# However, we must ensure we don't trigger real pygame mixer init.
# The best way is to patch 'command_line_conflict.scenes.menu.SoundSystem'.


class TestMenuScene(unittest.TestCase):
    def setUp(self):
        self.mock_game = MagicMock()
        self.mock_game.font = MagicMock()
        # Mock music manager
        self.mock_game.music_manager = MagicMock()

        # Patch SoundSystem to prevent real initialization
        self.patcher = patch("command_line_conflict.scenes.menu.SoundSystem")
        self.MockSoundSystem = self.patcher.start()

        self.scene = MenuScene(self.mock_game)

    def tearDown(self):
        self.patcher.stop()

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
        # Verify sound played
        self.scene.sound_system.play_sound.assert_called_with("click_select")

    def test_keyboard_navigation_plays_sound(self):
        # Start at 0
        self.scene.selected_option = 0

        event = MagicMock()
        event.type = pygame.KEYDOWN
        event.key = pygame.K_DOWN

        self.scene.handle_event(event)

        self.assertEqual(self.scene.selected_option, 1)
        self.scene.sound_system.play_sound.assert_called_with("click_select")

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
