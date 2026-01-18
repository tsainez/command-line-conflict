import stat
import unittest
from unittest.mock import MagicMock, patch

from command_line_conflict.maps.base import Map


class TestMapLoadLimit(unittest.TestCase):
    @patch("command_line_conflict.maps.base.os.fstat")
    @patch("command_line_conflict.maps.base.open")
    @patch("command_line_conflict.maps.base.os.path.commonpath")
    def test_load_from_file_reads_with_limit(self, mock_commonpath, mock_open, mock_fstat):
        """
        Test that load_from_file reads with a specific limit to prevent
        reading excessively large files that grew after the fstat check.
        """
        # Bypass path security check
        mock_commonpath.side_effect = lambda args: args[0]

        # Setup mock file
        mock_file = MagicMock()
        mock_file.fileno.return_value = 123
        mock_open.return_value.__enter__.return_value = mock_file

        # Setup fstat to return a valid small size
        mock_st = MagicMock()
        mock_st.st_size = 100  # Small size
        mock_st.st_mode = stat.S_IFREG
        mock_fstat.return_value = mock_st

        # Mock read to return valid JSON
        mock_file.read.return_value = '{"width": 10, "height": 10}'

        # Call load_from_file
        Map.load_from_file("test.json")

        # Verify that read was called with a limit
        # The limit is MAX_FILE_SIZE + 1 = 2*1024*1024 + 1
        expected_limit = Map.MAX_FILE_SIZE + 1

        # Check if read was called with the expected limit
        mock_file.read.assert_called_with(expected_limit)


if __name__ == "__main__":
    unittest.main()
