import json
import os
import tempfile
import unittest
from unittest.mock import patch

from command_line_conflict.utils.paths import atomic_save_json


class TestAtomicSave(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.target_file = os.path.join(self.test_dir, "data.json")

    def tearDown(self):
        import shutil
        shutil.rmtree(self.test_dir)

    def test_atomic_save_success(self):
        data = {"key": "value", "number": 123}
        atomic_save_json(self.target_file, data)

        self.assertTrue(os.path.exists(self.target_file))
        with open(self.target_file, "r") as f:
            loaded = json.load(f)
        self.assertEqual(loaded, data)

    def test_atomic_save_failure_cleanup(self):
        """Test that temp file is cleaned up if write fails."""
        data = {"key": "value"}

        # We start with no file
        self.assertFalse(os.path.exists(self.target_file))

        # Mock json.dump to raise an exception
        with patch("json.dump", side_effect=ValueError("Simulated serialization error")):
            with self.assertRaises(ValueError):
                atomic_save_json(self.target_file, data)

        # Target file should not exist
        self.assertFalse(os.path.exists(self.target_file))

        # Temp file should be cleaned up
        # We can verify this by checking if any file other than expected ones exists in dir
        # But since we don't know the exact name of temp file, checking len(os.listdir) is good
        self.assertEqual(len(os.listdir(self.test_dir)), 0)

    def test_atomic_save_overwrites(self):
        """Test that it overwrites existing file."""
        # Create initial file
        with open(self.target_file, "w") as f:
            f.write("old data")

        data = {"new": "data"}
        atomic_save_json(self.target_file, data)

        with open(self.target_file, "r") as f:
            content = json.load(f)
        self.assertEqual(content, data)

    def test_atomic_save_preserves_original_on_failure(self):
        """Test that original file is preserved if save fails."""
        # Create initial file
        with open(self.target_file, "w") as f:
            f.write('{"original": true}')

        data = {"new": "data"}

        # Mock json.dump to raise an exception
        with patch("json.dump", side_effect=ValueError("Simulated error")):
            with self.assertRaises(ValueError):
                atomic_save_json(self.target_file, data)

        # Original file should be untouched
        with open(self.target_file, "r") as f:
            content = f.read()
        self.assertEqual(content, '{"original": true}')
