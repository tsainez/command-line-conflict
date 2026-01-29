import unittest
import tempfile
import os
from command_line_conflict.campaign_manager import CampaignManager

class TestCampaignOverwrite(unittest.TestCase):
    def test_prevent_non_json_extension(self):
        """Test that CampaignManager rejects files without .json extension."""
        with tempfile.NamedTemporaryFile(suffix=".conf") as tmp:
            # Should raise ValueError because .conf is not .json
            # This assertion expects the code to be SECURE.
            # Currently it is INSECURE, so this test will FAIL.
            with self.assertRaises(ValueError) as cm:
                CampaignManager(save_file=tmp.name)

            self.assertIn("must have .json extension", str(cm.exception))

    def test_allow_json_extension(self):
        """Test that CampaignManager accepts .json extension."""
        with tempfile.NamedTemporaryFile(suffix=".json") as tmp:
            # Should not raise
            try:
                CampaignManager(save_file=tmp.name)
            except ValueError:
                self.fail("CampaignManager raised ValueError for valid .json file")

if __name__ == "__main__":
    unittest.main()
