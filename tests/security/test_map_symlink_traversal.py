import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from command_line_conflict.maps.base import Map


class TestMapSymlinkTraversal(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory structure for testing
        self.test_dir = tempfile.TemporaryDirectory()
        self.base_dir = Path(self.test_dir.name).resolve()
        self.allowed_dir = self.base_dir / "allowed"
        self.secret_dir = self.base_dir / "secret"

        self.allowed_dir.mkdir(exist_ok=True)
        self.secret_dir.mkdir(exist_ok=True)

        self.secret_file = self.secret_dir / "secret.json"
        with open(self.secret_file, "w") as f:
            f.write('{"secret": "data"}')

        self.symlink_file = self.allowed_dir / "link.json"

        try:
            os.symlink(self.secret_file, self.symlink_file)
        except OSError:
            self.skipTest("Symlinks not supported on this platform")

    def tearDown(self):
        self.test_dir.cleanup()

    def test_symlink_attack(self):
        m = Map(10, 10)

        # Patch with the absolute path of our temp directory
        with patch("command_line_conflict.utils.paths.get_user_data_dir", return_value=self.allowed_dir):
            try:
                # Pass the absolute path of the symlink
                m.save_to_file(str(self.symlink_file))
                vulnerable = True
            except ValueError:
                # Expected behavior: Security violation raised
                vulnerable = False

            self.assertFalse(vulnerable, "Map.save_to_file allowed writing to a symlink pointing outside allowed dirs!")


if __name__ == "__main__":
    unittest.main()
