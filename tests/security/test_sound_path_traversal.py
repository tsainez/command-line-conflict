import unittest
from unittest.mock import MagicMock, patch
import os
from command_line_conflict.systems.sound_system import SoundSystem

class TestSoundPathTraversal(unittest.TestCase):
    @patch("pygame.mixer.Sound")
    @patch("pygame.mixer.init")
    @patch("pygame.mixer.get_init", return_value=True)
    def test_path_traversal_prevention(self, mock_get_init, mock_init, mock_sound_class):
        """Verify that SoundSystem does not load files outside the sounds directory."""
        system = SoundSystem()

        # Payload trying to escape sounds directory
        payload = "../secret"

        # Patch exists to True so the system *tries* to load it if checks are insufficient
        with patch("os.path.exists", return_value=True):
             system.play_sound(payload)

        if mock_sound_class.called:
            # Get the path passed to Sound constructor
            call_args = mock_sound_class.call_args[0][0]
            normalized_arg = os.path.normpath(call_args)

            # The parent directory of the loaded file MUST be 'sounds'
            parent_dir = os.path.basename(os.path.dirname(normalized_arg))

            # If traversal worked, parent_dir would be 'command_line_conflict' (or whatever is above sounds)
            # instead of 'sounds'
            self.assertEqual(parent_dir, "sounds",
                             f"Security Violation: Attempted to load file outside 'sounds' directory: {normalized_arg}")

if __name__ == "__main__":
    unittest.main()
