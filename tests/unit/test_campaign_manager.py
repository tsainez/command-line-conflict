import unittest
from unittest.mock import patch

from command_line_conflict.campaign_manager import CampaignManager

class TestCampaignManager(unittest.TestCase):
    def setUp(self):
        # Prevent accessing user data dir and migrating
        self.patcher = patch("command_line_conflict.campaign_manager.get_user_data_dir")
        self.mock_get_dir = self.patcher.start()
        # Mock load_progress to prevent reading
        self.load_patcher = patch.object(CampaignManager, 'load_progress')
        self.mock_load = self.load_patcher.start()

    def tearDown(self):
        self.patcher.stop()
        self.load_patcher.stop()

    @patch("command_line_conflict.campaign_manager.atomic_save_json")
    def test_save_progress_success(self, mock_atomic_save):
        manager = CampaignManager("test_save.json")
        manager.completed_missions = ["mission_1"]

        manager.save_progress()

        mock_atomic_save.assert_called_once_with("test_save.json", {"completed_missions": ["mission_1"]})

    @patch("command_line_conflict.campaign_manager.atomic_save_json")
    @patch("command_line_conflict.campaign_manager.log")
    def test_save_progress_ioerror(self, mock_log, mock_atomic_save):
        manager = CampaignManager("test_save.json")
        manager.completed_missions = ["mission_1"]
        mock_atomic_save.side_effect = IOError("Test IOError")

        manager.save_progress()

        mock_atomic_save.assert_called_once_with("test_save.json", {"completed_missions": ["mission_1"]})
        mock_log.error.assert_called_once_with("Failed to save progress: Test IOError")
