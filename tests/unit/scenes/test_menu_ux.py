import pygame
import pytest
from unittest.mock import MagicMock, patch
from command_line_conflict.scenes.menu import MenuScene

# Test class for menu UX enhancements
class TestMenuUX:

    @pytest.fixture
    def mock_game(self):
        game = MagicMock()
        game.screen.get_width.return_value = 800
        game.screen.get_height.return_value = 600
        game.music_manager = MagicMock()
        return game

    def test_menu_visual_indicators(self, mock_game):
        """Test that the selected menu option has visual markers."""
        with patch('pygame.font.Font') as MockFont, \
             patch('command_line_conflict.scenes.menu.CampaignManager') as MockCampaignManager:

            # Setup mocks
            mock_font_instance = MockFont.return_value
            rendered_texts = []

            def mock_render(text, antialias, color):
                surface = MagicMock()
                surface.get_rect.return_value = pygame.Rect(0, 0, 100, 20)
                rendered_texts.append({'text': text, 'color': color})
                return surface

            mock_font_instance.render.side_effect = mock_render

            # Ensure CampaignManager has no progress so "New Game" is at index 0
            MockCampaignManager.return_value.completed_missions = []

            menu = MenuScene(mock_game)
            menu.draw(mock_game.screen)

            # Find the rendered text for the selected option (index 0 by default)
            # Default menu has "New Game" at index 0
            selected_option_render = next((r for r in rendered_texts if "New Game" in r['text']), None)

            assert selected_option_render is not None
            assert selected_option_render['text'] == "> New Game <"
            assert selected_option_render['color'] == (255, 255, 0)

            # Verify unselected option has no markers
            unselected_option_render = next((r for r in rendered_texts if "Map Editor" in r['text']), None)
            assert unselected_option_render is not None
            assert unselected_option_render['text'] == "Map Editor"
            assert unselected_option_render['color'] == (255, 255, 255)

    def test_menu_continue_campaign_option(self, mock_game):
        """Test that 'Continue Campaign' appears when progress exists."""
        with patch('pygame.font.Font') as MockFont, \
             patch('command_line_conflict.scenes.menu.CampaignManager') as MockCampaignManager:

            # Setup CampaignManager with progress
            mock_cm_instance = MockCampaignManager.return_value
            mock_cm_instance.completed_missions = ["mission_1"]

            # Setup Font mock to capture rendered text
            mock_font_instance = MockFont.return_value
            rendered_texts = []
            mock_font_instance.render.side_effect = lambda t, a, c: MagicMock()
            # We don't need to capture text here because we can inspect menu_options directly
            # invalidating previous test strategy because we want to test logic, not just rendering

            menu = MenuScene(mock_game)

            assert "Continue Campaign" in menu.menu_options
            assert menu.menu_options[0] == "Continue Campaign"
            assert "New Game" in menu.menu_options

    def test_menu_trigger_continue(self, mock_game):
        """Test that triggering 'Continue Campaign' switches to game scene."""
        with patch('pygame.font.Font'), \
             patch('command_line_conflict.scenes.menu.CampaignManager') as MockCampaignManager:

            mock_cm_instance = MockCampaignManager.return_value
            mock_cm_instance.completed_missions = ["mission_1"]

            menu = MenuScene(mock_game)

            # "Continue Campaign" is at index 0
            menu._trigger_option(0)

            mock_game.scene_manager.switch_to.assert_called_with("game")
