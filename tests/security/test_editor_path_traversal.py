import os
import unittest
from unittest.mock import MagicMock, patch

from command_line_conflict.ui.file_dialog import FileDialog

# pylint: disable=protected-access


class TestEditorPathTraversal(unittest.TestCase):
    def setUp(self):
        self.mouse_patcher = patch("pygame.mouse")
        self.mouse_patcher.start()

    def tearDown(self):
        self.mouse_patcher.stop()

    def test_path_traversal_sanitization(self):
        """
        Test that path traversal characters are stripped from the filename.
        """
        # Mock screen and font
        screen = MagicMock()
        font = MagicMock()
        font.render.return_value = MagicMock()

        initial_dir = os.path.join("tmp", "maps")
        dialog = FileDialog(screen, font, "Test", initial_dir, mode="save")

        # Simulate user inputting a path traversal string
        dialog.input_text = "../../../etc/passwd"

        # Confirm selection
        result = dialog._confirm_selection()

        # Expected behavior: os.path.basename should strip directory components
        # resulting in "passwd" (and extension added if needed, default .json)
        # So "passwd.json" inside initial_dir

        expected_filename = "passwd.json"
        expected_path = os.path.join(initial_dir, expected_filename)

        self.assertEqual(result, expected_path)

    def test_path_traversal_with_extension(self):
        screen = MagicMock()
        font = MagicMock()
        font.render.return_value = MagicMock()

        initial_dir = os.path.join("tmp", "maps")
        dialog = FileDialog(screen, font, "Test", initial_dir, mode="save")

        dialog.input_text = "../evil.json"

        result = dialog._confirm_selection()

        expected_path = os.path.join(initial_dir, "evil.json")
        self.assertEqual(result, expected_path)
