import unittest
import os
import json
import tempfile
from command_line_conflict.campaign_manager import CampaignManager

class TestCampaignManagerDoS(unittest.TestCase):
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.save_file = self.temp_file.name
        self.temp_file.close()

    def tearDown(self):
        if os.path.exists(self.save_file):
            os.remove(self.save_file)

    def test_load_large_file_prevention(self):
        # Create a file larger than the limit we intend to set (512KB)
        # We'll use 1MB to be sure.
        with open(self.save_file, "w") as f:
            f.write(" " * (1024 * 1024))

        # We expect an error log when loading fails due to size
        with self.assertLogs('Command Line Conflict', level='ERROR') as cm:
            manager = CampaignManager(save_file=self.save_file)

        # Verify that it didn't load (empty missions)
        self.assertEqual(len(manager.completed_missions), 0)
        # Verify log message
        self.assertTrue(any("exceeds maximum allowed size" in o for o in cm.output))

    def test_load_excessive_missions_truncation(self):
        # Create a valid JSON but with excessive items
        limit = 1000 # The limit we plan to set
        excess = 5000
        data = {
            "completed_missions": [f"mission_{i}" for i in range(excess)]
        }
        with open(self.save_file, "w") as f:
            json.dump(data, f)

        with self.assertLogs('Command Line Conflict', level='WARNING') as cm:
             manager = CampaignManager(save_file=self.save_file)

        # Should be truncated to the limit
        self.assertLessEqual(len(manager.completed_missions), limit)
        # Verify log message about truncation
        self.assertTrue(any("Too many completed missions" in o for o in cm.output))
