import unittest
import os
import shutil
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

# We need to import CampaignManager.
# Assuming PYTHONPATH is set correctly when running tests.
from command_line_conflict.campaign_manager import CampaignManager

class TestCampaignManagerSecurity(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_unsafe_path_raises_error(self):
        """Test that initializing CampaignManager with a path outside user data dir raises ValueError."""

        # We define "user data dir" as self.test_dir for this test
        with patch("command_line_conflict.campaign_manager.get_user_data_dir", return_value=Path(self.test_dir)):
            # Valid path
            valid_path = os.path.join(self.test_dir, "valid.json")
            try:
                CampaignManager(save_file=valid_path)
            except ValueError:
                self.fail("CampaignManager raised ValueError for a valid path within user data dir")

            # Invalid path (parent directory)
            # resolving path to ensure it is actually outside
            parent_dir = os.path.dirname(self.test_dir)
            invalid_path = os.path.join(parent_dir, "hacked.json")

            with self.assertRaises(ValueError, msg="Should raise ValueError for path outside user data dir"):
                CampaignManager(save_file=invalid_path)

    def test_non_json_extension_raises_error(self):
        """Test that CampaignManager raises ValueError for non-json extensions."""

        with patch("command_line_conflict.campaign_manager.get_user_data_dir", return_value=Path(self.test_dir)):
            invalid_ext_path = os.path.join(self.test_dir, "save.txt")

            with self.assertRaises(ValueError, msg="Should raise ValueError for non-json extension"):
                CampaignManager(save_file=invalid_ext_path)

if __name__ == '__main__':
    unittest.main()
