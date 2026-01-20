import unittest
from unittest.mock import MagicMock, patch, mock_open
import os
import stat
from command_line_conflict.maps.base import Map

class TestMapLoadingDoS(unittest.TestCase):
    """
    Tests for Denial of Service vulnerabilities in Map loading.
    Specifically checks for memory exhaustion attacks via large files.
    """

    def setUp(self):
        self.max_size = Map.MAX_FILE_SIZE

    @patch("command_line_conflict.maps.base.os.fstat")
    @patch("builtins.open")
    @patch("command_line_conflict.maps.base.os.path.realpath")
    @patch("command_line_conflict.utils.paths.get_user_data_dir")
    def test_load_from_file_reads_with_limit(self, mock_get_user_data, mock_realpath, mock_open_func, mock_fstat):
        """
        Verify that Map.load_from_file reads the file with an explicit limit
        instead of relying on json.load(f) which could read indefinitely
        if the file grows after the fstat check (TOCTOU).
        """
        # Setup mocks to pass validation
        filename = "test_map.json"
        abs_path = "/path/to/test_map.json"
        mock_realpath.return_value = abs_path

        # Mock allowed dirs
        mock_get_user_data.return_value = "/path/to"

        # Mock fstat to return valid size and regular file
        mock_st = MagicMock()
        mock_st.st_size = 100 # Safe size
        # Set st_mode to S_IFREG (regular file)
        mock_st.st_mode = stat.S_IFREG
        mock_fstat.return_value = mock_st

        # Mock file object
        mock_file = MagicMock()
        # Ensure the file object returned by open context manager is our mock
        mock_open_func.return_value.__enter__.return_value = mock_file

        # We simulate a "read" that returns valid JSON
        mock_file.read.return_value = '{"width": 10, "height": 10, "walls": []}'

        try:
             Map.load_from_file(filename)
        except Exception:
             pass

        # Verification:
        # The secure implementation should call f.read(limit)
        expected_limit = Map.MAX_FILE_SIZE + 1

        mock_file.read.assert_called_with(expected_limit)
