import os
import shutil
import tempfile
import unittest
from unittest.mock import patch

from command_line_conflict.campaign_manager import CampaignManager


class TestCampaignPathTraversal(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.allowed_dir = os.path.join(self.test_dir, "allowed")
        self.outside_dir = os.path.join(self.test_dir, "outside")

        os.makedirs(self.allowed_dir, exist_ok=True)
        os.makedirs(self.outside_dir, exist_ok=True)

        self.patcher = patch("command_line_conflict.campaign_manager.get_user_data_dir")
        self.mock_get_dir = self.patcher.start()
        self.mock_get_dir.return_value = self.allowed_dir

    def tearDown(self):
        self.patcher.stop()
        shutil.rmtree(self.test_dir)

    def test_save_path_traversal_blocked(self):
        """Test that saving campaign to a location outside allowed directories is blocked."""
        target_path = os.path.join(self.outside_dir, "pwned.json")

        with self.assertRaises(ValueError) as context:
            CampaignManager(save_file=target_path)

        self.assertIn("reside within the user data directory", str(context.exception))
        self.assertFalse(os.path.exists(target_path), "File should not be created for unauthorized path")

    def test_save_relative_traversal_blocked(self):
        """Test that using '..' to traverse directories is blocked."""
        # e.g. allowed/../outside/pwned.json -> outside/pwned.json
        target_path = os.path.join(self.allowed_dir, "..", "outside", "pwned.json")

        with self.assertRaises(ValueError) as context:
            CampaignManager(save_file=target_path)

        self.assertIn("reside within the user data directory", str(context.exception))

        # Resolve target path to ensure we check the exact spot it would have written
        abs_target = os.path.realpath(target_path)
        self.assertFalse(os.path.exists(abs_target), "File should not be created for unauthorized path")

    def test_invalid_extension_blocked(self):
        """Test that missing .json extension is blocked."""
        target_path = os.path.join(self.allowed_dir, "save_game.txt")

        with self.assertRaises(ValueError) as context:
            CampaignManager(save_file=target_path)

        self.assertIn(".json extension", str(context.exception))
        self.assertFalse(os.path.exists(target_path), "File should not be created with invalid extension")


if __name__ == "__main__":
    unittest.main()
