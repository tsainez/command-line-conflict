import unittest
from unittest.mock import MagicMock, patch

import pygame

from command_line_conflict.scenes.menu import MenuScene


class TestMenuUXQuit(unittest.TestCase):
    def setUp(self):
        self.mock_game = MagicMock()
        self.mock_game.font = MagicMock()
        self.mock_game.screen = MagicMock() # Needed for draw
        self.mock_game.music_manager = MagicMock()
        self.mock_game.running = True  # Simulate running state

        # Patch SoundSystem and CampaignManager
        self.patcher_sound = patch("command_line_conflict.scenes.menu.SoundSystem")
        self.MockSoundSystem = self.patcher_sound.start()

        self.patcher_campaign = patch("command_line_conflict.scenes.menu.CampaignManager")
        self.MockCampaignManager = self.patcher_campaign.start()
        self.MockCampaignManager.return_value.completed_missions = []

        self.scene = MenuScene(self.mock_game)

    def tearDown(self):
        self.patcher_sound.stop()
        self.patcher_campaign.stop()

    def test_quit_double_confirmation_flow(self):
        """Test the full double-confirmation flow for quitting."""
        quit_index = self.scene.menu_options.index("Quit")
        self.scene.selected_option = quit_index

        # 1. Initial state
        self.assertFalse(getattr(self.scene, "confirm_quit", False), "Should start false")

        # 2. First Trigger (First Click/Enter)
        self.scene._trigger_option(quit_index)

        # Expectation: Game still running, confirmation active
        self.assertTrue(self.mock_game.running, "Game should not quit on first click")
        self.assertTrue(getattr(self.scene, "confirm_quit", False), "Confirmation state should be True")

        # 3. Second Trigger (Confirmation)
        self.scene._trigger_option(quit_index)

        # Expectation: Game stops running
        self.assertFalse(self.mock_game.running, "Game should quit on second click")

    def test_navigation_cancels_confirmation(self):
        """Test that navigating away cancels the quit confirmation."""
        quit_index = self.scene.menu_options.index("Quit")

        # 1. Activate confirmation
        self.scene.selected_option = quit_index
        self.scene._trigger_option(quit_index)
        self.assertTrue(self.scene.confirm_quit)

        # 2. Simulate User Navigating Up (to Options)
        event = MagicMock()
        event.type = pygame.KEYDOWN
        event.key = pygame.K_UP

        self.scene.handle_event(event)

        self.assertFalse(self.scene.confirm_quit, "Navigating away should cancel confirmation")

    def test_draw_changes_text(self):
        """Test that draw renders 'Confirm Quit?' when active."""
        quit_index = self.scene.menu_options.index("Quit")
        self.scene.selected_option = quit_index # Must be selected for the text logic to trigger
        self.scene.confirm_quit = True

        # Mock _get_text_surface because it's cached and difficult to check otherwise
        # Or check the blit calls on screen

        self.mock_game.screen.blit = MagicMock()

        # We need to make sure _get_text_surface returns something we can identify
        # But _get_text_surface calls self.option_font.render.
        # Since we are testing if the LOGIC passes the right text to _get_text_surface,
        # we can patch _get_text_surface if we could, but it's an instance method with lru_cache.

        # Instead, let's look at what is rendered.
        # The code calculates `display_text`.
        # If I can't easily patch lru_cache, I can rely on the fact that
        # `option_font.render` will be called with the text.

        # CLEAR CACHE to ensure render is called
        self.scene._get_text_surface.cache_clear()

        self.scene.option_font.render = MagicMock()
        self.scene.option_font.render.return_value = MagicMock() # Return a mock surface

        self.scene.draw(self.mock_game.screen)

        # Check if "Confirm Quit?" was rendered
        render_calls = self.scene.option_font.render.call_args_list
        found_confirm_text = False
        for call in render_calls:
            # call[0][0] is the text
            # The logic adds "> " and " <"
            if "> Confirm Quit? <" in call[0][0]:
                found_confirm_text = True
                break

        self.assertTrue(found_confirm_text, "Should render '> Confirm Quit? <' text")

if __name__ == "__main__":
    unittest.main()
