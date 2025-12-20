import os
import unittest
from unittest.mock import MagicMock, patch

from command_line_conflict.scenes.editor import EditorScene


class TestEditorPathTraversal(unittest.TestCase):
    def setUp(self):
        self.mock_game = MagicMock()
        self.mock_game.font = MagicMock()
        self.mock_game.screen.get_size.return_value = (800, 600)

    @patch("command_line_conflict.scenes.editor.input")
    @patch("command_line_conflict.scenes.editor.os.path.exists")
    @patch("command_line_conflict.scenes.editor.Map")
    def test_save_map_path_traversal_fix(self, mock_map_cls, mock_exists, mock_input):
        """
        Test that path traversal is blocked in save_map.
        """
        # We need to construct EditorScene.
        # Since we mock Map class, EditorScene will use the mock.
        editor = EditorScene(self.mock_game)

        # Force console mode
        with patch("command_line_conflict.scenes.editor.HAS_TKINTER", False):
            # Simulate user entering a path traversal filename
            mock_input.return_value = "../evil_map"
            mock_exists.return_value = True

            editor.save_map()

            editor.map.save_to_file.assert_called()
            args, _ = editor.map.save_to_file.call_args
            saved_path = args[0]

            normalized_path = os.path.normpath(saved_path)

            # We expect the path to be sanitized to "evil_map.json" inside custom dir
            # Vulnerable code produces: .../maps/custom/../evil_map.json -> .../maps/evil_map.json
            # Fixed code produces: .../maps/custom/evil_map.json

            expected_suffix = os.path.join("maps", "custom", "evil_map.json")
            self.assertTrue(
                normalized_path.endswith(expected_suffix),
                f"Path traversal detected! Path: {normalized_path}",
            )

    @patch("command_line_conflict.scenes.editor.input")
    @patch("command_line_conflict.scenes.editor.os.path.exists")
    @patch("command_line_conflict.scenes.editor.Map")
    def test_load_map_path_traversal_fix(self, mock_map_cls, mock_exists, mock_input):
        """
        Test that path traversal is blocked in load_map.
        """
        editor = EditorScene(self.mock_game)

        with patch("command_line_conflict.scenes.editor.HAS_TKINTER", False):
            mock_input.return_value = "../secret_file"
            mock_exists.return_value = True

            editor.load_map()

            mock_map_cls.load_from_file.assert_called()
            args, _ = mock_map_cls.load_from_file.call_args
            loaded_path = args[0]

            normalized_path = os.path.normpath(loaded_path)
            expected_suffix = os.path.join("maps", "custom", "secret_file.json")
            self.assertTrue(
                normalized_path.endswith(expected_suffix),
                f"Path traversal detected in load! Path: {normalized_path}",
            )

    @patch("command_line_conflict.scenes.editor.input")
    @patch("command_line_conflict.scenes.editor.os.path.exists")
    @patch("command_line_conflict.scenes.editor.Map")
    def test_save_map_valid_filename(self, mock_map_cls, mock_exists, mock_input):
        editor = EditorScene(self.mock_game)
        with patch("command_line_conflict.scenes.editor.HAS_TKINTER", False):
            mock_input.return_value = "good_map"
            mock_exists.return_value = True

            editor.save_map()

            editor.map.save_to_file.assert_called()
            args, _ = editor.map.save_to_file.call_args
            saved_path = args[0]
            normalized_path = os.path.normpath(saved_path)
            expected_suffix = os.path.join("maps", "custom", "good_map.json")
            self.assertTrue(normalized_path.endswith(expected_suffix))
