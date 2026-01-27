from unittest.mock import MagicMock, patch

import pygame
import pytest

from command_line_conflict.scenes.editor import EditorScene


class TestEditorToolbar:
    @pytest.fixture
    def editor_context(self):
        mock_game = MagicMock()
        mock_game.screen.get_size.return_value = (800, 600)
        mock_game.screen.get_width.return_value = 800
        mock_game.font = MagicMock()
        mock_game.scene_manager = MagicMock()

        with patch("command_line_conflict.scenes.editor.Map"):
            with patch("command_line_conflict.scenes.editor.FileDialog") as MockFileDialog:
                scene = EditorScene(mock_game)
                scene.map.width = 40
                scene.map.height = 30
                yield scene, MockFileDialog

    def test_buttons_initialized(self, editor_context):
        editor_scene, _ = editor_context
        assert len(editor_scene.buttons) == 3
        labels = [btn["text"] for btn in editor_scene.buttons]
        assert "Save" in labels
        assert "Load" in labels
        assert "Menu" in labels

    def test_hover_updates_cursor(self, editor_context):
        editor_scene, _ = editor_context
        # Position over the "Save" button (10, 10, 80, 40)
        event = MagicMock()
        event.type = pygame.MOUSEMOTION
        event.pos = (20, 20)

        with patch("pygame.mouse.set_cursor") as mock_set_cursor:
            editor_scene.handle_event(event)
            mock_set_cursor.assert_called_with(pygame.SYSTEM_CURSOR_HAND)

    def test_click_save_opens_dialog(self, editor_context):
        editor_scene, MockFileDialog = editor_context
        # Position over "Save" button
        event = MagicMock()
        event.type = pygame.MOUSEBUTTONDOWN
        event.button = 1
        event.pos = (20, 20)

        with patch.object(editor_scene, "handle_click") as mock_map_click:
            editor_scene.handle_event(event)

            assert MockFileDialog.called
            assert editor_scene.file_dialog is not None
            mock_map_click.assert_not_called()

    def test_click_load_opens_dialog(self, editor_context):
        editor_scene, MockFileDialog = editor_context
        # Position over "Load" button (100, 10, 80, 40)
        event = MagicMock()
        event.type = pygame.MOUSEBUTTONDOWN
        event.button = 1
        event.pos = (120, 20)

        # Reset mock calls from init
        MockFileDialog.reset_mock()

        with patch.object(editor_scene, "handle_click") as mock_map_click:
            editor_scene.handle_event(event)

            assert MockFileDialog.called
            assert editor_scene.file_dialog is not None
            mock_map_click.assert_not_called()

    def test_click_menu_returns(self, editor_context):
        editor_scene, _ = editor_context
        # Position over "Menu" button (190, 10, 80, 40)
        event = MagicMock()
        event.type = pygame.MOUSEBUTTONDOWN
        event.button = 1
        event.pos = (210, 20)

        with patch.object(editor_scene, "handle_click") as mock_map_click:
            editor_scene.handle_event(event)

            # Verify scene switch
            editor_scene.game.scene_manager.switch_to.assert_called_with("menu")
            mock_map_click.assert_not_called()

    def test_click_outside_ui_edits_map(self, editor_context):
        editor_scene, _ = editor_context
        # Position below UI (> 60)
        event = MagicMock()
        event.type = pygame.MOUSEBUTTONDOWN
        event.button = 1
        event.pos = (100, 100)

        with patch.object(editor_scene, "handle_click") as mock_map_click:
            editor_scene.handle_event(event)
            mock_map_click.assert_called_once_with((100, 100))
