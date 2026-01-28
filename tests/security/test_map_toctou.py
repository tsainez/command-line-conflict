import unittest
from unittest.mock import mock_open, patch

from command_line_conflict.maps.base import Map


class TestMapTOCTOU(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open)
    @patch("os.makedirs")
    @patch("command_line_conflict.maps.base.os.path.realpath")
    @patch("command_line_conflict.maps.base.os.path.dirname")
    @patch("command_line_conflict.maps.base.os.path.abspath")
    # Patch where it is imported in command_line_conflict.maps.base
    @patch("command_line_conflict.utils.paths.get_user_data_dir")
    @patch("command_line_conflict.utils.paths.tempfile.mkstemp")
    @patch("command_line_conflict.utils.paths.os.close")
    @patch("command_line_conflict.utils.paths.os.replace")
    @patch("command_line_conflict.utils.paths.os.fsync")
    @patch("command_line_conflict.utils.paths.os.fdopen")
    def test_save_to_file_uses_resolved_path(
        self,
        mock_fdopen,
        mock_fsync,
        mock_replace,
        mock_close,
        mock_mkstemp,
        mock_get_user_data,
        mock_abspath,
        mock_dirname,
        mock_realpath,
        mock_makedirs,
        mock_file,
    ):
        """
        Test that Map.save_to_file calls atomic save flow with resolved paths.
        """
        # Setup mocks
        filename = "some_symlink.json"
        resolved_path = "/secure/path/to/real_file.json"
        temp_path = "/secure/path/to/temp_file"

        # Setup allowed directories to pass validation
        maps_dir = "/secure/path/to"
        user_data_dir = "/user/data"

        mock_abspath.return_value = "/secure/path/to/base.py"
        mock_dirname.return_value = maps_dir
        mock_get_user_data.return_value = user_data_dir
        mock_mkstemp.return_value = (123, temp_path)

        # Setup fdopen context manager
        mock_fd = mock_open().return_value
        mock_fd.fileno.return_value = 123
        mock_fdopen.return_value.__enter__.return_value = mock_fd

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

        # Assert mkstemp was called
        mock_mkstemp.assert_called()

        # Assert replace was called with resolved path
        mock_replace.assert_called_with(temp_path, resolved_path)

    @patch("command_line_conflict.utils.paths.atomic_save_json")
    @patch("command_line_conflict.maps.base.os.makedirs")
    @patch("command_line_conflict.maps.base.os.path.realpath")
    @patch("command_line_conflict.maps.base.os.path.dirname")
    @patch("command_line_conflict.maps.base.os.path.abspath")
    @patch("command_line_conflict.utils.paths.get_user_data_dir")
    def test_save_to_file_uses_resolved_path_patched_atomic(
        self, mock_get_user_data, mock_abspath, mock_dirname, mock_realpath, mock_makedirs, mock_atomic_save
    ):
        # Setup mocks
        filename = "some_symlink.json"
        resolved_path = "/secure/path/to/real_file.json"

        # Setup allowed directories to pass validation
        maps_dir = "/secure/path/to"
        user_data_dir = "/user/data"

        mock_abspath.return_value = "/secure/path/to/base.py"
        mock_dirname.return_value = maps_dir
        mock_get_user_data.return_value = user_data_dir

        def realpath_side_effect(path):
            if path == filename:
                return resolved_path
            return str(path)

        mock_realpath.side_effect = realpath_side_effect

        m = Map(10, 10)
        m.save_to_file(filename)

        mock_atomic_save.assert_called_with(resolved_path, m.to_dict())
