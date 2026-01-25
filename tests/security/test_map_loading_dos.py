import stat
import unittest
from unittest.mock import MagicMock, patch

from command_line_conflict.maps.base import Map


class TestMapLoadingDoS(unittest.TestCase):
    @patch("command_line_conflict.maps.base.os.fstat")
    @patch("builtins.open")
    @patch("command_line_conflict.maps.base.os.path.commonpath")
    def test_load_from_file_reads_with_limit(self, mock_commonpath, mock_open, mock_fstat):
        """
        Verify that Map.load_from_file reads the file with a strict limit
        to prevent memory exhaustion DoS if the file grows during a race condition.
        """
        # Bypass path security check
        def side_effect(args):
            return args[0]
        mock_commonpath.side_effect = side_effect

        # Mock file object
        mock_file = MagicMock()
        mock_file.fileno.return_value = 123

        # Setup context manager for open
        mock_open.return_value.__enter__.return_value = mock_file

        # Mock fstat to simulate a "valid" small file initially
        mock_st = MagicMock()
        mock_st.st_size = 100  # Small size
        mock_st.st_mode = stat.S_IFREG
        mock_fstat.return_value = mock_st

        # Mock read to return valid JSON
        mock_file.read.return_value = '{"width": 10, "height": 10}'

        # Call load_from_file
        try:
            Map.load_from_file("test_map.json")
        except ValueError:
            pass # We don't care if it fails parsing or whatever, we care about the read call

        # Assert read was called with MAX_FILE_SIZE + 1
        # The current implementation uses json.load(f), which calls f.read() repeatedly or with buffers.
        # It likely won't call it with this specific limit.
        mock_file.read.assert_called_with(Map.MAX_FILE_SIZE + 1)
