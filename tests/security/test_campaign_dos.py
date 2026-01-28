import unittest
from unittest.mock import MagicMock, patch
import os
import stat
from command_line_conflict.campaign_manager import CampaignManager

class TestCampaignManagerDos(unittest.TestCase):
    @patch("builtins.open")
    @patch("os.path.exists")
    @patch("os.fstat")
    def test_load_progress_non_regular_file(self, mock_fstat, mock_exists, mock_open):
        # Setup mocks
        mock_exists.return_value = True

        # Mock file object
        mock_file = MagicMock()
        mock_file.read.return_value = "{}" # Return valid empty JSON so it doesn't crash on json.loads
        mock_open.return_value.__enter__.return_value = mock_file

        # Simulate a FIFO/special file (not S_ISREG)
        # st_mode = 0 means it's definitely not a regular file
        mock_st = MagicMock()
        mock_st.st_mode = stat.S_IFIFO  # Named pipe
        mock_st.st_size = 0
        mock_fstat.return_value = mock_st

        # Initialize CampaignManager
        # It will try to load progress in __init__
        cm = CampaignManager(save_file="fifo_pipe")

        # Verification
        # In the FIXED version, it should check fstat, see it's not regular, and NOT read.

        mock_file.read.assert_not_called()

if __name__ == "__main__":
    unittest.main()
