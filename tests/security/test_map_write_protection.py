import os
import shutil
import unittest
import tempfile
from unittest.mock import patch
from pathlib import Path

import command_line_conflict.maps.base
from command_line_conflict.maps.base import Map

class TestMapWriteProtection(unittest.TestCase):
    def setUp(self):
        self.map = Map(10, 10)
        # Determine the actual maps directory used by the application
        self.maps_dir = os.path.dirname(os.path.abspath(command_line_conflict.maps.base.__file__))

        # Create a temp directory for user data mock using tempfile to avoid collisions
        self.test_dir_obj = tempfile.TemporaryDirectory()
        self.test_dir = Path(self.test_dir_obj.name)
        self.user_data_dir = self.test_dir / "user_data"
        self.user_data_dir.mkdir()

    def tearDown(self):
        self.test_dir_obj.cleanup()

    def test_save_to_app_dir_blocked(self):
        """Test that saving to the application's map directory is blocked."""
        # This path is inside the application source tree
        forbidden_path = os.path.join(self.maps_dir, "malicious_map.json")

        # We need to mock get_user_data_dir to ensure it's DIFFERENT from maps_dir
        # verifying that ONLY user_data_dir is allowed.
        with patch("command_line_conflict.utils.paths.get_user_data_dir", return_value=self.user_data_dir):
             with self.assertRaises(ValueError) as cm:
                self.map.save_to_file(forbidden_path)

             self.assertIn("unauthorized location", str(cm.exception))

    def test_save_to_user_data_dir_allowed(self):
        """Test that saving to the user data directory is allowed."""
        allowed_path = self.user_data_dir / "safe_map.json"

        with patch("command_line_conflict.utils.paths.get_user_data_dir", return_value=self.user_data_dir):
            # Should not raise
            self.map.save_to_file(str(allowed_path))

            self.assertTrue(allowed_path.exists())

if __name__ == "__main__":
    unittest.main()
