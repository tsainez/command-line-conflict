import os
from command_line_conflict.campaign_manager import CampaignManager

# Test malicious path
manager = CampaignManager(save_file="/tmp/malicious_save.txt")
manager.save_progress()

if os.path.exists("/tmp/malicious_save.txt"):
    print("VULNERABLE!")
else:
    print("SAFE")
