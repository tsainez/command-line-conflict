import unittest
import os
import shutil
import tempfile
from command_line_conflict.campaign_manager import CampaignManager

class TestCampaignRuntimeDoS(unittest.TestCase):
    def setUp(self):
        # Create a temp directory for the save file
        self.test_dir = tempfile.mkdtemp()
        self.save_file = os.path.join(self.test_dir, "test_save.json")

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_unbounded_mission_growth(self):
        """Test that we CANNOT add more missions than the limit allows (Fix verification)."""
        manager = CampaignManager(save_file=self.save_file)

        # Current limit is 1000
        limit = CampaignManager.MAX_MISSIONS_COUNT

        # Try to add more than the limit
        for i in range(limit + 50):
            manager.complete_mission(f"mission_{i}")

        # With the fix, the count should be capped at the limit
        self.assertLessEqual(len(manager.completed_missions), limit, "Fix verified: Mission count capped at limit during runtime")
        self.assertEqual(len(manager.completed_missions), limit)

    def test_huge_mission_id(self):
        """Test adding a mission ID with excessive length (Fix verification)."""
        manager = CampaignManager(save_file=self.save_file)

        huge_id = "A" * (CampaignManager.MAX_MISSION_ID_LENGTH + 10)

        # This should now fail (gracefully)
        manager.complete_mission(huge_id)

        self.assertNotIn(huge_id, manager.completed_missions)

        # The save file might not exist if save was never triggered
        if os.path.exists(self.save_file):
             self.assertLess(os.path.getsize(self.save_file), 1000)
