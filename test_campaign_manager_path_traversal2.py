import os
import shutil
from command_line_conflict.campaign_manager import CampaignManager

# Test malicious path
cm = CampaignManager(save_file="/tmp/some_malicious_path.json")
cm.save_progress()

if os.path.exists("/tmp/some_malicious_path.json"):
    print("VULNERABLE to arbitrary writes!")
else:
    print("SAFE")
