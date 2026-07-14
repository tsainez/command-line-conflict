import unittest
from unittest.mock import patch

from command_line_conflict.campaign_manager import CampaignManager


class TestCampaignManager(unittest.TestCase):
    @patch("command_line_conflict.campaign_manager.log")
    @patch("command_line_conflict.campaign_manager.atomic_save_json")
    def test_save_progress_io_error(self, mock_atomic_save, mock_log):
        mock_atomic_save.side_effect = IOError("Disk full")
        manager = CampaignManager(save_file="dummy.json")
        manager.save_progress()
        mock_log.error.assert_called_once()
        self.assertIn("Failed to save progress: Disk full", mock_log.error.call_args[0][0])
