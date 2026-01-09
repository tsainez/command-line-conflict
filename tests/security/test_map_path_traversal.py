import shutil
import unittest
from pathlib import Path

from command_line_conflict.maps.base import Map


class TestMapSecurity(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory structure for testing
        self.base_dir = Path("tmp/security_test")
        self.outside_dir = self.base_dir / "outside"
        self.outside_dir.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        if self.base_dir.exists():
            shutil.rmtree(self.base_dir)

    def test_save_path_traversal_blocked(self):
        """Test that saving a map to a location outside allowed directories is blocked."""
        m = Map(10, 10)

        # Path that traverses out of any allowed directory
        # The allowed directories are command_line_conflict/maps and user_data_dir
        # This path points to tmp/security_test/outside/pwned.json
        target_path = self.outside_dir / "pwned.json"

        # This MUST raise ValueError now that the fix is in place
        with self.assertRaises(ValueError):
            m.save_to_file(str(target_path))

        # Ensure the file was NOT created
        self.assertFalse(target_path.exists(), "File should not be created for unauthorized path")

    def test_save_relative_traversal_blocked(self):
        """Test that using '..' to traverse directories is blocked."""
        m = Map(10, 10)

        # Attempt to break out to a temporary directory
        target_path = self.outside_dir / "pwned_rel.json"

        with self.assertRaises(ValueError):
            m.save_to_file(str(target_path))

        self.assertFalse(target_path.exists(), "File should not be created for unauthorized path")


if __name__ == "__main__":
    unittest.main()
