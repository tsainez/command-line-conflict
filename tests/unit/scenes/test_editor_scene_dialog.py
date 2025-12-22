from unittest.mock import MagicMock, patch

import pygame
import pytest

from command_line_conflict.scenes.editor import EditorScene


class TestEditorSceneDialog:

    @pytest.fixture
    def mock_game(self):
        game = MagicMock()
        game.font = MagicMock()
        game.screen = MagicMock()
        return game

    @pytest.fixture
    def editor_scene(self, mock_game):
        with patch("command_line_conflict.scenes.editor.Map"):
            scene = EditorScene(mock_game)
        return scene

    def test_open_save_dialog(self, editor_scene):
        editor_scene.open_save_dialog()
        assert editor_scene.file_dialog is not None
        assert editor_scene.file_dialog.mode == "save"
        # Check camera stopped
        for k, v in editor_scene.camera_movement.items():
            assert v is False

    def test_open_load_dialog(self, editor_scene):
        editor_scene.open_load_dialog()
        assert editor_scene.file_dialog is not None
        assert editor_scene.file_dialog.mode == "load"

    def test_dialog_interaction(self, editor_scene):
        editor_scene.open_save_dialog()

        # Mock file dialog event handling
        mock_result = "test_map.json"
        editor_scene.file_dialog = MagicMock()
        editor_scene.file_dialog.active = True
        editor_scene.file_dialog.mode = "save"
        editor_scene.file_dialog.handle_event.return_value = mock_result

        # Mock map save
        editor_scene.map = MagicMock()

        event = MagicMock()
        editor_scene.handle_event(event)

        editor_scene.map.save_to_file.assert_called_with(mock_result)
        assert editor_scene.file_dialog is None

    def test_dialog_cancel(self, editor_scene):
        editor_scene.open_save_dialog()

        # Mock cancel (returns None, sets active=False)
        mock_dialog = MagicMock()
        mock_dialog.active = True

        def side_effect(event):
            mock_dialog.active = False
            return None

        mock_dialog.handle_event.side_effect = side_effect
        editor_scene.file_dialog = mock_dialog

        event = MagicMock()
        editor_scene.handle_event(event)

        assert editor_scene.file_dialog is None

    def test_key_triggers(self, editor_scene):
        # 's' key
        event = MagicMock()
        event.type = pygame.KEYDOWN
        event.key = pygame.K_s

        with patch.object(editor_scene, "open_save_dialog") as mock_open:
            editor_scene.handle_event(event)
            mock_open.assert_called_once()

        # 'l' key
        event.key = pygame.K_l
        with patch.object(editor_scene, "open_load_dialog") as mock_open:
            editor_scene.handle_event(event)
            mock_open.assert_called_once()
