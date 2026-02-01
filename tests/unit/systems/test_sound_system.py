import unittest
from unittest.mock import MagicMock, patch

from command_line_conflict.systems.sound_system import SoundSystem


class TestSoundSystem(unittest.TestCase):
    def setUp(self):
        self.game_state = MagicMock()
        self.game_state.event_queue = []

    @patch("pygame.mixer.Sound")
    @patch("pygame.mixer.init")
    @patch("pygame.mixer.get_init", return_value=True)
    @patch("os.path.exists", return_value=True)
    def test_play_sound(self, mock_exists, mock_get_init, mock_init, mock_sound_class):
        system = SoundSystem()

        # Setup event
        self.game_state.event_queue = [{"type": "sound", "data": {"name": "test_sound"}}]

        # Mock sound object
        mock_sound_instance = MagicMock()
        mock_sound_class.return_value = mock_sound_instance

        system.update(self.game_state)

        # Check that it was called with a path ending in sounds/test_sound.wav or .ogg
        args, _ = mock_sound_class.call_args
        # With our changes, it tries .wav first. Since os.path.exists returns True for everything, it finds .wav
        # Use replace to handle Windows backslashes
        path = args[0].replace("\\", "/")
        self.assertTrue(path.endswith("sounds/test_sound.wav") or path.endswith("sounds/test_sound.ogg"))
        mock_sound_instance.play.assert_called()

    @patch("pygame.mixer.Sound")
    @patch("pygame.mixer.init")
    @patch("pygame.mixer.get_init", return_value=True)
    @patch("os.path.exists", return_value=False)
    def test_missing_sound_file(self, mock_exists, mock_get_init, mock_init, mock_sound_class):
        system = SoundSystem()

        # Setup event
        self.game_state.event_queue = [{"type": "sound", "data": {"name": "missing_sound"}}]

        system.update(self.game_state)

        mock_sound_class.assert_not_called()

    @patch("pygame.mixer.Sound")
    @patch("pygame.mixer.init")
    @patch("pygame.mixer.get_init", return_value=True)
    @patch("os.path.exists", return_value=True)
    def test_caching(self, mock_exists, mock_get_init, mock_init, mock_sound_class):
        system = SoundSystem()

        self.game_state.event_queue = [
            {"type": "sound", "data": {"name": "cached_sound"}},
            {"type": "sound", "data": {"name": "cached_sound"}},
        ]

        system.update(self.game_state)

        # Should only load once
        mock_sound_class.assert_called_once()
        args, _ = mock_sound_class.call_args
        # With our changes, it tries .wav first. Since os.path.exists returns True for everything, it finds .wav
        path = args[0].replace("\\", "/")
        self.assertTrue(path.endswith("sounds/cached_sound.wav") or path.endswith("sounds/cached_sound.ogg"))
        # Should play twice (once per update loop iteration if we were looping, but update iterates list)
        # Actually update iterates over list.
        # First iteration: play "cached_sound". Loads it.
        # Second iteration: play "cached_sound". Uses cache.
        self.assertEqual(system.sounds["cached_sound"].play.call_count, 2)


if __name__ == "__main__":
    unittest.main()
