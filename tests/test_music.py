import unittest
from unittest.mock import patch

from command_line_conflict import config
from command_line_conflict.music import MusicManager


class TestMusicManager(unittest.TestCase):
    def setUp(self):
        # We need to initialize pygame mixer or mock it
        # Since we are testing logic, mocking is better/safer for CI
        pass

    @patch("pygame.mixer.music")
    @patch("pygame.mixer.init")
    @patch("pygame.mixer.get_init", return_value=False)
    @patch("os.path.getsize", return_value=1024)
    @patch("os.path.isfile", return_value=True)
    @patch("os.path.exists", return_value=True)
    def test_play_music(self, mock_exists, mock_isfile, mock_getsize, mock_get_init, mock_init, mock_music):
        manager = MusicManager()
        manager.play("test.ogg")

        mock_music.load.assert_called_with("test.ogg")
        mock_music.play.assert_called_with(-1)
        self.assertEqual(manager.current_track, "test.ogg")

    @patch("pygame.mixer.music")
    @patch("pygame.mixer.init")
    @patch("pygame.mixer.get_init", return_value=True)
    @patch("os.path.getsize", return_value=1024)
    @patch("os.path.isfile", return_value=True)
    @patch("os.path.exists", return_value=True)
    def test_play_music_already_playing_same_track(
        self, mock_exists, mock_isfile, mock_getsize, mock_get_init, mock_init, mock_music
    ):
        manager = MusicManager()
        manager.current_track = "test.ogg"
        mock_music.get_busy.return_value = True

        manager.play("test.ogg")

        mock_music.load.assert_not_called()
        mock_music.play.assert_not_called()

    @patch("pygame.mixer.music")
    @patch("pygame.mixer.init")
    @patch("pygame.mixer.get_init", return_value=True)
    def test_stop_music(self, mock_get_init, mock_init, mock_music):
        manager = MusicManager()
        manager.current_track = "something.ogg"
        manager.stop()

        mock_music.stop.assert_called()
        self.assertIsNone(manager.current_track)

    @patch("pygame.mixer.music")
    @patch("pygame.mixer.init")
    @patch("pygame.mixer.get_init", return_value=True)
    def test_set_volume(self, mock_get_init, mock_init, mock_music):
        manager = MusicManager()
        manager.set_volume(0.8)

        mock_music.set_volume.assert_called_with(0.8)
        self.assertEqual(manager.volume, 0.8)

    @patch("pygame.mixer.music")
    @patch("pygame.mixer.init")
    @patch("pygame.mixer.get_init", return_value=True)
    @patch("os.path.exists", return_value=False)
    def test_missing_file(self, mock_exists, mock_get_init, mock_init, mock_music):
        manager = MusicManager()
        manager.play("missing.ogg")

        mock_music.load.assert_not_called()
        self.assertIsNone(manager.current_track)

    @patch("pygame.mixer.music")
    @patch("pygame.mixer.init")
    @patch("pygame.mixer.get_init", return_value=True)
    @patch("os.path.getsize")
    @patch("os.path.isfile", return_value=True)
    @patch("os.path.exists", return_value=True)
    def test_rejects_oversized_file(self, mock_exists, mock_isfile, mock_getsize, mock_get_init, mock_init, mock_music):
        mock_getsize.return_value = config.MAX_AUDIO_FILE_SIZE + 1
        manager = MusicManager()
        manager.play("huge.ogg")

        mock_music.load.assert_not_called()
        self.assertIsNone(manager.current_track)


if __name__ == "__main__":
    unittest.main()
