from unittest.mock import MagicMock
import pytest
from command_line_conflict.scenes.game import GameScene
import command_line_conflict.config as config

class MockGame:
    def __init__(self):
        self.screen = None
        self.font = None
        self.music_manager = MagicMock()

def test_debug_mode_logs_cheats(mocker):
    # Arrange
    mocker.patch("command_line_conflict.config.DEBUG", True)
    mock_logger = mocker.patch("command_line_conflict.scenes.game.log")

    game = MockGame()

    # Act
    GameScene(game)

    # Assert
    # Collect all log messages
    messages = []
    for call in mock_logger.info.call_args_list:
        messages.append(call.args[0])

    combined_log = "\n".join(messages)

    assert "F1: Toggle Reveal Map" in combined_log
    assert "F2: Toggle God Mode" in combined_log
    assert "TAB: Switch Player" in combined_log
    assert "1-6: Spawn Units" in combined_log

def test_no_debug_mode_no_cheats_log(mocker):
    # Arrange
    mocker.patch("command_line_conflict.config.DEBUG", False)
    mock_logger = mocker.patch("command_line_conflict.scenes.game.log")

    game = MockGame()

    # Act
    GameScene(game)

    # Assert
    messages = []
    for call in mock_logger.info.call_args_list:
        messages.append(call.args[0])

    combined_log = "\n".join(messages)

    assert "F1: Toggle Reveal Map" not in combined_log
