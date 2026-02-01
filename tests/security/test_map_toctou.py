import os
import unittest
from unittest.mock import ANY, patch

from command_line_conflict.maps.base import Map


class TestMapTOCTOU(unittest.TestCase):
    @patch("command_line_conflict.utils.paths.atomic_save_json")
    @patch("command_line_conflict.maps.base.os.makedirs")
    @patch("command_line_conflict.maps.base.os.path.realpath")
    @patch("command_line_conflict.maps.base.os.path.dirname")
    @patch("command_line_conflict.utils.paths.get_user_data_dir")
    def test_save_to_file_uses_resolved_path(
        self,
        mock_get_user_data,
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
        # Setup mocks with platform-independent absolute paths
        # On Windows, os.path.abspath will add drive letter (e.g. C:\)
        # On Linux/Mac, it will just root it (e.g. /)

        # Use a fake root for testing that works with commonpath
        if os.name == "nt":
            root = "C:\\"
        else:
            root = "/"

        filename = "some_symlink.json"

        # Use os.path.join to ensure correct separators
        resolved_path = os.path.join(root, "secure", "path", "to", "real_file.json")
        maps_dir = os.path.join(root, "secure", "path", "to")
        user_data_dir = os.path.join(root, "user", "data")

        mock_dirname.return_value = maps_dir
        mock_get_user_data.return_value = user_data_dir

        # mock_realpath should return resolved_path for filename
        def realpath_side_effect(path):
            if path == filename:
                return resolved_path
            # For other paths (maps_dir, user_data_dir), return them as-is
            # Note: The code calls realpath on get_user_data_dir result and maps dir result too.
            # We need to handle those or just return string.
            # Since our mocks return absolute paths already, str(path) is fine.
            return str(path)

        mock_realpath.side_effect = realpath_side_effect

        # We also need to patch os.path.commonpath because on Windows it might be strict
        # if the mocked paths don't match actual filesystem reality (though with our paths they should be fine)
        # However, it's safer to let real commonpath run if our paths are valid.
        # "C:\secure\path\to\real_file.json" starts with "C:\secure\path\to" so it should work.

        m = Map(10, 10)

        # Call save_to_file
        m.save_to_file(filename)

        # Assert atomic_save_json was called with resolved_path
        mock_atomic_save.assert_called_with(resolved_path, ANY)


if __name__ == "__main__":
    unittest.main()
