from unittest.mock import MagicMock, patch

import pygame
import pytest

from command_line_conflict.scenes.editor import EditorScene


class TestEditorUX:
    @pytest.fixture
    def editor_scene(self):
        mock_game = MagicMock()
        mock_game.screen.get_size.return_value = (800, 600)
        mock_game.font = MagicMock()

        with patch("command_line_conflict.scenes.editor.Map"):
            scene = EditorScene(mock_game)
            scene.map.width = 40
            scene.map.height = 30
            return scene

    def test_cursor_changes_over_grid(self, editor_scene):
        """Test that cursor changes to CROSSHAIR when over the grid."""
        event = MagicMock()
        event.type = pygame.MOUSEMOTION
        event.pos = (400, 300)  # Center of screen

        with patch("pygame.mouse.set_cursor") as mock_set_cursor:
            editor_scene.handle_event(event)
            # This will fail initially as the logic isn't there
            mock_set_cursor.assert_called_with(pygame.SYSTEM_CURSOR_CROSSHAIR)

    def test_cursor_changes_over_ui(self, editor_scene):
        """Test that cursor changes to ARROW when over the UI area but not on a button."""
        event = MagicMock()
        event.type = pygame.MOUSEMOTION
        event.pos = (5, 5)  # Top left, avoiding buttons at (10, 10)

        with patch("pygame.mouse.set_cursor") as mock_set_cursor:
            editor_scene.handle_event(event)
            mock_set_cursor.assert_called_with(pygame.SYSTEM_CURSOR_ARROW)
