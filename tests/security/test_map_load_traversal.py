import unittest
from unittest.mock import MagicMock, patch

from command_line_conflict.maps.base import Map


class TestMapLoadTraversal(unittest.TestCase):
    @patch("json.load")
    @patch("command_line_conflict.maps.base.open")
    @patch("command_line_conflict.maps.base.os.stat")
    @patch("command_line_conflict.maps.base.os.path.realpath")
    def test_load_from_unauthorized_location(self, mock_realpath, mock_stat, mock_open, mock_json_load):
        """Verify that loading map from unauthorized location raises ValueError."""
        # Setup mocks to simulate a valid file in an unauthorized location
        unauthorized_path = "/etc/passwd"  # Example unauthorized path

        # We mock realpath to just return the input, simulating it resolving to /etc/passwd
        mock_realpath.side_effect = lambda x: x

        # Mock stat to look like a regular small file
        mock_st = MagicMock()
        mock_st.st_size = 100
        mock_st.st_mode = 0o100644  # Regular file
        mock_stat.return_value = mock_st

        # Mock open/json to return valid map data
        mock_json_load.return_value = {"width": 10, "height": 10, "walls": []}

        # This call SHOULD fail with ValueError due to path traversal check
        try:
            Map.load_from_file(unauthorized_path)
            self.fail("Map.load_from_file did not raise ValueError for unauthorized path")
        except ValueError as e:
            # Check if it's the security error
            self.assertIn("unauthorized location", str(e))
