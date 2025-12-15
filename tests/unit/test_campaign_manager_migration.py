import os
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from command_line_conflict.campaign_manager import (
    DEFAULT_SAVE_FILENAME,
    CampaignManager,
)


class TestCampaignManagerMigration(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.temp_data_dir = Path(self.test_dir) / "data"

        self.patcher = patch("command_line_conflict.campaign_manager.get_user_data_dir")
        self.mock_get_dir = self.patcher.start()
        self.mock_get_dir.return_value = self.temp_data_dir

        # We need to change CWD to a temp dir so we don't write to actual CWD
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)

    def tearDown(self):
        self.patcher.stop()
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)

    def test_init_creates_directory(self):
        CampaignManager()
        self.assertTrue(self.temp_data_dir.exists())

    def test_migration_legacy_file(self):
        # Create a dummy legacy save file in current directory (which is self.test_dir)
        with open(DEFAULT_SAVE_FILENAME, "w") as f:
            f.write("{}")

        manager = CampaignManager()

        # Check it moved
        self.assertFalse(os.path.exists(DEFAULT_SAVE_FILENAME))
        self.assertTrue((self.temp_data_dir / DEFAULT_SAVE_FILENAME).exists())
        self.assertEqual(
            manager.save_file, str(self.temp_data_dir / DEFAULT_SAVE_FILENAME)
        )

    def test_no_migration_if_dest_exists(self):
        # Create legacy file
        with open(DEFAULT_SAVE_FILENAME, "w") as f:
            f.write('{"legacy": true}')

        # Create destination directory and file
        self.temp_data_dir.mkdir(parents=True)
        with open(self.temp_data_dir / DEFAULT_SAVE_FILENAME, "w") as f:
            f.write('{"new": true}')

        CampaignManager()

        # Legacy file should still exist (no overwrite)
        self.assertTrue(os.path.exists(DEFAULT_SAVE_FILENAME))
        # Dest file should remain unchanged
        with open(self.temp_data_dir / DEFAULT_SAVE_FILENAME, "r") as f:
            content = f.read()
            self.assertIn('"new": true', content)

    def test_explicit_path_no_migration(self):
        # Even if legacy file exists, providing explicit path should use that path
        with open(DEFAULT_SAVE_FILENAME, "w") as f:
            f.write("{}")

        custom_path = "custom_save.json"
        manager = CampaignManager(custom_path)

        self.assertEqual(manager.save_file, custom_path)
        # Legacy file untouched
        self.assertTrue(os.path.exists(DEFAULT_SAVE_FILENAME))
