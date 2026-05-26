import unittest
from unittest.mock import MagicMock, patch

from command_line_conflict.steam_integration import SteamIntegration


class TestSteamIntegrationSecurity(unittest.TestCase):
    @patch("command_line_conflict.steam_integration.log")
    def test_unlock_achievement_input_validation(self, mock_log):
        # Create instance and mock steam object to pretend it's initialized
        integration = SteamIntegration()
        integration.initialized = True
        integration.steam = MagicMock()

        # Test valid achievement names
        valid_names = [
            "GAME_START",
            "ACHIEVEMENT_1",
            "a" * 64,
            "12345",
            "_",
        ]

        for name in valid_names:
            integration.unlock_achievement(name)
            integration.steam.SetAchievement.assert_called_with(name)
            integration.steam.SetAchievement.reset_mock()

        # Test invalid achievement names (should be rejected)
        invalid_names = [
            "GAME START",  # contains space
            "ACHIEVEMENT-1",  # contains dash
            "a" * 65,  # too long
            "; DROP TABLE users;",  # SQL injection attempt
            "<script>alert(1)</script>",  # XSS attempt
            "../../etc/passwd",  # Path traversal attempt
            "",  # empty string
            None,  # Not a string
            123,  # Not a string
        ]

        for name in invalid_names:
            try:
                integration.unlock_achievement(name)
                integration.steam.SetAchievement.assert_not_called()
            except TypeError:
                pass

            mock_log.warning.assert_called()


if __name__ == "__main__":
    unittest.main()
