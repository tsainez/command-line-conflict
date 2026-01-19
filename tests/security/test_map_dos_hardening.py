import unittest
from unittest.mock import MagicMock, patch, mock_open
import stat
import json
from command_line_conflict.maps.base import Map

class TestMapDoSHardening(unittest.TestCase):
    @patch("command_line_conflict.maps.base.os.path.commonpath")
    @patch("command_line_conflict.maps.base.os.fstat")
    @patch("command_line_conflict.maps.base.open", new_callable=mock_open, read_data='{"width": 10, "height": 10}')
    def test_load_enforces_read_limit(self, mock_open_func, mock_fstat, mock_commonpath):
        """Test that load_from_file reads with an explicit limit."""
        # Allow path check
        mock_commonpath.side_effect = lambda args: args[0]

        # Pass fstat check (size within limit)
        mock_st = MagicMock()
        mock_st.st_size = 100
        mock_st.st_mode = stat.S_IFREG
        mock_fstat.return_value = mock_st

        Map.load_from_file("secure_map.json")

        handle = mock_open_func.return_value.__enter__.return_value

        # We expect read to be called with MAX_FILE_SIZE + 1
        expected_limit = Map.MAX_FILE_SIZE + 1

        # Check calls.
        # Note: json.load(f) calls f.read() (usually without args or with chunks).
        # We want to assert it IS called with expected_limit.
        handle.read.assert_called_with(expected_limit)

    @patch("command_line_conflict.maps.base.os.path.commonpath")
    @patch("command_line_conflict.maps.base.os.fstat")
    @patch("command_line_conflict.maps.base.open", new_callable=mock_open)
    def test_load_raises_on_actual_content_overflow(self, mock_open_func, mock_fstat, mock_commonpath):
        """Test that load_from_file raises ValueError if read content exceeds limit, even if fstat was OK."""
        # Allow path check
        mock_commonpath.side_effect = lambda args: args[0]

        # Pass fstat check (simulate lying file or TOCTOU: st_size is small)
        mock_st = MagicMock()
        mock_st.st_size = 100
        mock_st.st_mode = stat.S_IFREG
        mock_fstat.return_value = mock_st

        # But actual read returns more data than limit
        limit = Map.MAX_FILE_SIZE
        # Return content larger than limit
        large_content = "a" * (limit + 10)

        handle = mock_open_func.return_value.__enter__.return_value
        handle.read.return_value = large_content

        with self.assertRaises(ValueError) as cm:
            Map.load_from_file("attack.json")

        self.assertIn("exceeds maximum allowed size", str(cm.exception))
