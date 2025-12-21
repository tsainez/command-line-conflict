# pylint: disable=redefined-outer-name
import sys
from unittest.mock import MagicMock, patch

import pytest

from command_line_conflict.steam_integration import SteamIntegration


@pytest.fixture
def mock_log():
    with patch("command_line_conflict.steam_integration.log") as mock:
        yield mock


def test_steam_integration_init_success(mock_log):
    mock_steam = MagicMock()
    mock_steam_instance = MagicMock()
    mock_steam.STEAMWORKS.return_value = mock_steam_instance

    with patch.dict(sys.modules, {"steamworks": mock_steam}):
        steam = SteamIntegration()

        assert steam.initialized is True
        mock_steam.STEAMWORKS.assert_called_once()
        mock_steam_instance.initialize.assert_called_once()
        mock_log.info.assert_called_with("Steamworks initialized successfully.")


def test_steam_integration_init_failure(mock_log):
    # Simulate ImportError
    with patch.dict(sys.modules):
        if "steamworks" in sys.modules:
            del sys.modules["steamworks"]

        with patch("builtins.__import__", side_effect=ImportError):
            steam = SteamIntegration()
            assert steam.initialized is False
            mock_log.warning.assert_called_with("steamworks module not found. Steam integration disabled.")


def test_unlock_achievement(mock_log):
    mock_steam = MagicMock()
    mock_steam_instance = MagicMock()
    mock_steam.STEAMWORKS.return_value = mock_steam_instance

    with patch.dict(sys.modules, {"steamworks": mock_steam}):
        steam = SteamIntegration()
        steam.unlock_achievement("TEST_ACHIEVEMENT")

        mock_steam_instance.SetAchievement.assert_called_with("TEST_ACHIEVEMENT")
        mock_steam_instance.StoreStats.assert_called_once()
        mock_log.info.assert_called_with("Unlocked achievement: TEST_ACHIEVEMENT")


def test_unlock_achievement_not_initialized(mock_log):
    with patch("builtins.__import__", side_effect=ImportError):
        steam = SteamIntegration()
        steam.unlock_achievement("TEST_ACHIEVEMENT")
        assert steam.initialized is False
        mock_log.debug.assert_called_with("Steam not initialized. Skipping achievement: TEST_ACHIEVEMENT")


def test_update(mock_log):
    mock_steam = MagicMock()
    mock_steam_instance = MagicMock()
    mock_steam.STEAMWORKS.return_value = mock_steam_instance

    with patch.dict(sys.modules, {"steamworks": mock_steam}):
        steam = SteamIntegration()
        steam.update()

        mock_steam_instance.RunCallbacks.assert_called_once()
