import json
import os
import unittest
from pathlib import Path
from unittest.mock import patch

from command_line_conflict.campaign_manager import CampaignManager


class TestCampaignRaceCondition(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path("tmp_test/security_race")
        self.test_dir.mkdir(parents=True, exist_ok=True)
        self.save_file = self.test_dir / "large_save.json"

        # Security Fix: Mock get_user_data_dir to allow test path
        self.patcher = patch("command_line_conflict.campaign_manager.get_user_data_dir", return_value=self.test_dir.resolve())
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()
        if self.save_file.exists():
            os.remove(self.save_file)
        if self.test_dir.exists():
            os.rmdir(self.test_dir)

    def test_load_progress_race_condition(self):
        """
        Test that CampaignManager.load_progress is vulnerable to TOCTOU.
        We create a large file but mock os.path.getsize to return a small size.
        Without the fix, the file will be loaded.
        With the fix, it should be rejected during the read phase.
        """
        # 1. Create a file larger than MAX_SAVE_FILE_SIZE (512KB)
        max_size = CampaignManager.MAX_SAVE_FILE_SIZE
        # Create content that exceeds the limit.
        # Note: json.dumps adds quotes, so we just need enough padding.
        padding = " " * (max_size + 1000)
        json_content = json.dumps({"completed_missions": ["mission_pwned"], "padding": padding})

        with open(self.save_file, "w") as f:
            f.write(json_content)

        # Verify file is actually big
        actual_size = os.path.getsize(self.save_file)
        self.assertGreater(actual_size, max_size, "Setup error: Test file is not large enough")

        # 2. Mock os.path.getsize to return a small safe size (e.g. 100 bytes)
        # This simulates the check passing (Time Of Check)
        # while the real file is huge (Time Of Use)
        # NOTE: If the implementation correctly uses fstat on the open file,
        # patching os.path.getsize shouldn't matter, but it confirms we aren't relying on os.path.getsize.
        with patch("os.path.getsize", return_value=100):
            cm = CampaignManager(save_file=str(self.save_file))

            # 3. Assert that "mission_pwned" was NOT loaded.
            # If the vulnerability exists, the file is read fully and parsed, so "mission_pwned" will be present.
            # If the fix is working, the read will stop or error out, and missions won't be loaded.

            # EXPECTATION: This assertion fails BEFORE the fix.
            self.assertNotIn(
                "mission_pwned",
                cm.completed_missions,
                "VULNERABILITY DETECTED: Large file was loaded! TOCTOU race condition allows bypassing size limits.",
            )


if __name__ == "__main__":
    unittest.main()
