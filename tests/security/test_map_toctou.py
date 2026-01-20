import unittest
from unittest.mock import mock_open, patch, MagicMock

from command_line_conflict.maps.base import Map


class TestMapTOCTOU(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open)
    @patch("os.makedirs")
    @patch("command_line_conflict.maps.base.os.path.realpath")
    @patch("command_line_conflict.maps.base.os.path.dirname")
    @patch("command_line_conflict.maps.base.os.path.abspath")
    # Patch where it is imported in command_line_conflict.maps.base
    @patch("command_line_conflict.utils.paths.get_user_data_dir")
    # We need to patch os.path.abspath in tempfile too because atomic_save_json uses tempfile.mkstemp
    @patch("tempfile.mkstemp")
    @patch("command_line_conflict.utils.paths.os.replace")
    @patch("command_line_conflict.utils.paths.os.fsync")
    @patch("command_line_conflict.utils.paths.os.fdopen")
    def test_save_to_file_uses_resolved_path(
        self,
        mock_fdopen,
        mock_fsync,
        mock_replace,
        mock_mkstemp,
        mock_get_user_data,
        mock_abspath,
        mock_dirname,
        mock_realpath,
        mock_makedirs,
        mock_file,
    ):
        """
        Test that Map.save_to_file calls open() with the resolved absolute path,
        not the input filename, to prevent TOCTOU vulnerabilities where the
        symlink changes after validation but before opening.
        """
        # Setup mocks
        filename = "some_symlink.json"
        resolved_path = "/secure/path/to/real_file.json"

        # Setup allowed directories to pass validation
        maps_dir = "/secure/path/to"
        user_data_dir = "/user/data"

        mock_abspath.return_value = "/secure/path/to/base.py"
        mock_dirname.return_value = maps_dir
        mock_get_user_data.return_value = user_data_dir

        # Setup mkstemp to return a dummy fd and path
        mock_mkstemp.return_value = (123, "/secure/path/to/tmp_file")

        # Setup fdopen to return a file object that supports write
        mock_temp_file = MagicMock()
        mock_fdopen.return_value.__enter__.return_value = mock_temp_file

        # mock_realpath should return resolved_path for filename
        def realpath_side_effect(path):
            if path == filename:
                return resolved_path
            # For other paths (maps_dir, user_data_dir), return them as-is
            return str(path)

        mock_realpath.side_effect = realpath_side_effect

        m = Map(10, 10)

        # Call save_to_file
        m.save_to_file(filename)

        # Verification:
        # atomic_save_json is called with resolved_path.
        # It creates a temp file, writes to it, and then replaces.
        # We can assert that os.replace was called with resolved_path as destination.

        mock_replace.assert_called_with("/secure/path/to/tmp_file", resolved_path)


if __name__ == "__main__":
    unittest.main()
