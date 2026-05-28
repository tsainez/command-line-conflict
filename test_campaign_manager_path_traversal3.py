import os
import tempfile
from command_line_conflict.campaign_manager import CampaignManager

test_dir = tempfile.mkdtemp()
malicious_path = os.path.join(test_dir, "malicious.txt")

try:
    cm = CampaignManager(save_file=malicious_path)
    cm.save_progress()
    print("VULNERABLE: Save succeeded at", malicious_path)
except ValueError as e:
    print("SAFE: ValueError raised:", e)
except Exception as e:
    print("UNKNOWN EXCEPTION:", e)
