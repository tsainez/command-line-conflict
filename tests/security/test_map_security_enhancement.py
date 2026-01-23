import os
import shutil
import unittest
from pathlib import Path
from unittest.mock import patch

from command_line_conflict.maps.base import Map


class TestMapSecurityEnhancement(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory structure for testing
        self.base_dir = Path("tmp/security_test_enhancement")
        # Use absolute path to ensure realpath matches
        self.base_dir = self.base_dir.resolve()

        self.user_data_dir = self.base_dir / "user_data"
        self.source_dir = self.base_dir / "source"

        self.user_data_dir.mkdir(parents=True, exist_ok=True)
        self.source_dir.mkdir(parents=True, exist_ok=True)

        # Mock get_user_data_dir to return our temp user data dir
        self.patcher = patch("command_line_conflict.utils.paths.get_user_data_dir")
        self.mock_get_user_data = self.patcher.start()
        # Return as Path object, similar to actual function
        self.mock_get_user_data.return_value = self.user_data_dir

    def tearDown(self):
        self.patcher.stop()
        if self.base_dir.exists():
            shutil.rmtree(self.base_dir)

    @patch("command_line_conflict.utils.paths.atomic_save_json")
    def test_save_to_user_data_allowed(self, mock_save):
        """Test that saving to user data directory is allowed."""
        m = Map(10, 10)
        target_path = self.user_data_dir / "valid_save.json"

        # Should not raise
        m.save_to_file(str(target_path))

        # Verify atomic_save_json was called
        mock_save.assert_called_once()

    @patch("command_line_conflict.utils.paths.atomic_save_json")
    def test_save_to_arbitrary_dir_blocked(self, mock_save):
        """Test that saving to an arbitrary directory (mimicking source dir) is blocked."""
        m = Map(10, 10)
        target_path = self.source_dir / "malicious_save.json"

        # Should raise ValueError because it's not in user_data_dir
        with self.assertRaises(ValueError) as cm:
            m.save_to_file(str(target_path))

        self.assertIn("unauthorized location", str(cm.exception))
        # Verify atomic_save_json was NOT called
        mock_save.assert_not_called()


if __name__ == "__main__":
    unittest.main()
