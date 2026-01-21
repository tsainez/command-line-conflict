import unittest
from unittest.mock import MagicMock, patch

from command_line_conflict.maps.base import Map


class TestMapTOCTOU(unittest.TestCase):
    @patch("command_line_conflict.utils.paths.atomic_save_json")
    @patch("os.makedirs")
    @patch("command_line_conflict.maps.base.os.path.realpath")
    @patch("command_line_conflict.maps.base.os.path.dirname")
    @patch("command_line_conflict.maps.base.os.path.abspath")
    # Patch where it is imported in command_line_conflict.maps.base
    @patch("command_line_conflict.utils.paths.get_user_data_dir")
    def test_save_to_file_uses_resolved_path(
        self,
        mock_get_user_data,
        mock_abspath,
        mock_dirname,
        mock_realpath,
        mock_makedirs,
        mock_atomic_save,
    ):
        """
        Test that Map.save_to_file calls atomic_save_json() with the resolved absolute path,
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

        # Assert atomic_save_json was called with resolved_path
        mock_atomic_save.assert_called_with(resolved_path, m.to_dict())


if __name__ == "__main__":
    unittest.main()
