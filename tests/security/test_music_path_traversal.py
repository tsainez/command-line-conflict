import os
import unittest
from unittest.mock import patch, MagicMock

from command_line_conflict.music import MusicManager


class TestMusicPathTraversal(unittest.TestCase):
    def setUp(self):
        # Patch pygame mixer initialization
        self.patchers = [
            patch("pygame.mixer.init"),
            patch("pygame.mixer.get_init", return_value=True),
            patch("pygame.mixer.music")
        ]
        for p in self.patchers:
            p.start()

        self.music_manager = MusicManager()

    def tearDown(self):
        for p in self.patchers:
            p.stop()

    @patch("pygame.mixer.music.load")
    @patch("pygame.mixer.music.play")
    def test_path_traversal_attack_blocked(self, mock_play, mock_load):
        """Test that attempting to load a non-music file is blocked."""
        target_file = "requirements.txt"  # Exists in root, but has invalid extension

        self.music_manager.play(target_file)

        # Verification: It should NOT have called load
        mock_load.assert_not_called()

    @patch("pygame.mixer.music.load")
    @patch("pygame.mixer.music.play")
    def test_path_traversal_directory_blocked(self, mock_play, mock_load):
        """Test that attempting to load a file outside the project root is blocked."""
        # Mock a file path that is definitely outside
        # Even if we give it a valid extension
        target_file_with_ext = "/etc/passwd.mp3"

        self.music_manager.play(target_file_with_ext)

        # Verification: It should NOT have called load
        mock_load.assert_not_called()

    @patch("pygame.mixer.music.load")
    @patch("pygame.mixer.music.play")
    def test_valid_music_loading(self, mock_play, mock_load):
        """Test that valid music files within the project are allowed."""
        # Create a dummy music file path that is valid relative to CWD
        target_file = "music/menu_theme.ogg"

        # We need to mock os.path.exists so it thinks this file exists
        with patch("os.path.exists", return_value=True):
            # Also assume abspath works as expected for current dir
            self.music_manager.play(target_file)

        # Verification: It SHOULD have called load
        mock_load.assert_called_with(target_file)

if __name__ == "__main__":
    unittest.main()
