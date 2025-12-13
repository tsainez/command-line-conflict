import unittest
from unittest.mock import MagicMock, patch
import os
import pygame
from command_line_conflict.scenes.editor import EditorScene
from command_line_conflict.maps.base import Map

class TestPathTraversal(unittest.TestCase):
    def setUp(self):
        self.mock_game = MagicMock()
        self.mock_game.font = MagicMock()
        self.mock_game.screen.get_size.return_value = (800, 600)

        # We need to ensure EditorScene can init without errors
        with patch('command_line_conflict.maps.base.Map.load_from_file', side_effect=FileNotFoundError), \
             patch('pygame.font.SysFont'):
            self.scene = EditorScene(self.mock_game)

    @patch('command_line_conflict.maps.base.Map.save_to_file')
    @patch('builtins.input', return_value="../pwned.json")
    @patch('command_line_conflict.scenes.editor.HAS_TKINTER', False)
    def test_save_path_traversal(self, mock_input, mock_save):
        """
        Test that validates if path traversal is prevented via console input.
        """
        # Call save_map which uses input()
        self.scene.save_map()

        # Check what path was passed to save_to_file
        if mock_save.called:
            args, _ = mock_save.call_args
            saved_path = args[0]

            # Resolve absolute paths
            abs_saved_path = os.path.abspath(saved_path)

            # Determine the intended directory
            # Based on EditorScene code: os.path.join("command_line_conflict", "maps", "custom")
            expected_dir = os.path.abspath(os.path.join("command_line_conflict", "maps", "custom"))

            # Check if saved_path is within expected_dir
            self.assertTrue(abs_saved_path.startswith(expected_dir),
                            f"Path traversal detected! {abs_saved_path} is not in {expected_dir}")
        else:
             self.fail("save_to_file was not called")

    @patch('command_line_conflict.maps.base.Map.load_from_file')
    @patch('builtins.input', return_value="../pwned.json")
    @patch('command_line_conflict.scenes.editor.HAS_TKINTER', False)
    def test_load_path_traversal(self, mock_input, mock_load):
        """
        Test that validates if path traversal is prevented via console input during load.
        """
        # Call load_map which uses input()
        self.scene.load_map()

        # Check what path was passed to load_from_file
        if mock_load.called:
            args, _ = mock_load.call_args
            load_path = args[0]

            # Resolve absolute paths
            abs_load_path = os.path.abspath(load_path)

            # Determine the intended directory
            expected_dir = os.path.abspath(os.path.join("command_line_conflict", "maps", "custom"))

            # Check if load_path is within expected_dir
            self.assertTrue(abs_load_path.startswith(expected_dir),
                            f"Path traversal detected! {abs_load_path} is not in {expected_dir}")
        else:
             self.fail("load_from_file was not called")
