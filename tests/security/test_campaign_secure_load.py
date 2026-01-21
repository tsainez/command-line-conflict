import os
import stat
import unittest
from unittest.mock import MagicMock, mock_open, patch

from command_line_conflict.campaign_manager import CampaignManager

class TestCampaignSecureLoad(unittest.TestCase):
    def test_load_progress_enforces_regular_file(self):
        """
        Test that load_progress verifies the file is a regular file using fstat
        before reading content, to prevent reading from special files.
        """
        save_file = "dummy_save.json"

        # Mock content that looks valid
        valid_json = '{"completed_missions": ["mission_1"]}'

        m_open = mock_open(read_data=valid_json)
        # Configure fileno for the mock file
        m_file = m_open.return_value
        m_file.fileno.return_value = 10

        # Mock os.fstat to simulate a NON-regular file (e.g., a block device)
        # S_IFBLK means block device
        mode = stat.S_IFBLK | 0o644
        mock_stat_result = os.stat_result((mode, 0, 0, 0, 0, 0, 100, 0, 0, 0))

        with patch("builtins.open", m_open), \
             patch("os.fstat", return_value=mock_stat_result) as m_fstat, \
             patch("os.path.exists", return_value=True): # Mock exists for the current implementation

            cm = CampaignManager(save_file=save_file)

            # We expect that fstat was called
            # NOTE: This assertion is expected to FAIL on the current codebase
            if not m_fstat.called:
                print("FAIL: os.fstat was not called as expected.")

            self.assertTrue(m_fstat.called, "Security check: os.fstat should be called to verify file type.")
            m_fstat.assert_called_with(10)

            # We expect that because it's a block device, we did NOT load the missions
            # currently, without the fix, it WILL load the missions because it ignores fstat
            self.assertEqual(cm.completed_missions, [], "Should not load data from non-regular file")

if __name__ == "__main__":
    unittest.main()
