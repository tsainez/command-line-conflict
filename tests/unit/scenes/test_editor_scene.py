import unittest
from unittest.mock import MagicMock, patch

from command_line_conflict.maps.base import Map
from command_line_conflict.scenes.editor import EditorScene


class TestEditorScene(unittest.TestCase):
    def setUp(self):
        self.mock_game = MagicMock()
        self.mock_game.font = MagicMock()
        self.mock_game.screen.get_size.return_value = (800, 600)

        # Patch Map.load_from_file to fail so we get a blank map
        # Also patch pygame.font.SysFont
        with patch(
            "command_line_conflict.maps.base.Map.load_from_file",
            side_effect=FileNotFoundError,
        ), patch("pygame.font.SysFont"):
            self.scene = EditorScene(self.mock_game)

    def test_initialization(self):
        self.assertIsInstance(self.scene.map, Map)
        self.assertEqual(self.scene.map.width, 40)

    def test_handle_click_toggle_wall(self):
        # Mock camera to return 5, 5
        self.scene.camera.screen_to_grid = MagicMock(return_value=(5, 5))

        # Initial state: no wall
        self.assertFalse(self.scene.map.is_blocked(5, 5))

        # Click
        self.scene.handle_click((100, 100))
        self.assertTrue(self.scene.map.is_blocked(5, 5))

        # Click again
        self.scene.handle_click((100, 100))
        self.assertFalse(self.scene.map.is_blocked(5, 5))

    @patch("command_line_conflict.maps.base.Map.save_to_file")
    @patch("command_line_conflict.scenes.editor.filedialog.asksaveasfilename")
    @patch("command_line_conflict.scenes.editor.tk.Tk")
    @patch("command_line_conflict.scenes.editor.HAS_TKINTER", True)
    def test_save_map_tkinter(self, mock_tk, mock_asksave, mock_save):
        mock_asksave.return_value = "path/to/save.json"

        # Setup mock Tk instance
        mock_root = MagicMock()
        mock_tk.return_value = mock_root

        self.scene.save_map()

        mock_tk.assert_called()
        mock_root.withdraw.assert_called()
        mock_asksave.assert_called()
        mock_root.destroy.assert_called()
        mock_save.assert_called_with("path/to/save.json")

    @patch("command_line_conflict.maps.base.Map.save_to_file")
    @patch("command_line_conflict.scenes.editor.filedialog.asksaveasfilename")
    @patch("command_line_conflict.scenes.editor.tk.Tk")
    @patch("command_line_conflict.scenes.editor.HAS_TKINTER", True)
    def test_save_map_cancel(self, mock_tk, mock_asksave, mock_save):
        mock_asksave.return_value = ""  # User cancelled
        mock_tk.return_value = MagicMock()

        self.scene.save_map()

        mock_save.assert_not_called()

    @patch("command_line_conflict.maps.base.Map.save_to_file")
    @patch("builtins.input", return_value="console_save")
    @patch("command_line_conflict.scenes.editor.HAS_TKINTER", False)
    def test_save_map_console(self, mock_input, mock_save):
        self.scene.save_map()

        mock_input.assert_called()
        # Should save to default_dir/console_save.json
        args, _ = mock_save.call_args
        self.assertTrue(args[0].endswith("console_save.json"))

    @patch("command_line_conflict.maps.base.Map.load_from_file")
    @patch("command_line_conflict.scenes.editor.filedialog.askopenfilename")
    @patch("command_line_conflict.scenes.editor.tk.Tk")
    @patch("command_line_conflict.scenes.editor.HAS_TKINTER", True)
    def test_load_map_tkinter(self, mock_tk, mock_askopen, mock_load):
        mock_askopen.return_value = "path/to/load.json"
        mock_tk.return_value = MagicMock()

        self.scene.load_map()

        mock_load.assert_called_with("path/to/load.json")

    @patch("command_line_conflict.maps.base.Map.load_from_file")
    @patch("builtins.input", return_value="console_load")
    @patch("command_line_conflict.scenes.editor.HAS_TKINTER", False)
    def test_load_map_console(self, mock_input, mock_load):
        self.scene.load_map()

        mock_input.assert_called()
        args, _ = mock_load.call_args
        self.assertTrue(args[0].endswith("console_load.json"))
