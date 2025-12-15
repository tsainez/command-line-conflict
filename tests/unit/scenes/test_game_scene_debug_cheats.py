from unittest.mock import MagicMock

import pytest

import command_line_conflict.config as config
from command_line_conflict.scenes.game import GameScene


class MockGame:
    def __init__(self):
        self.screen = MagicMock()
        self.font = MagicMock()
        self.music_manager = MagicMock()
        # Mock screen get_size for grid drawing logic
        self.screen.get_size.return_value = (800, 600)


def test_debug_mode_logs_cheats(mocker):
    # Arrange
    mocker.patch("command_line_conflict.config.DEBUG", True)
    mock_logger = mocker.patch("command_line_conflict.scenes.game.log")

    game = MockGame()

    # Act
    GameScene(game)

    # Assert
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


def test_debug_mode_does_not_disable_fog_of_war(mocker):
    # Arrange
    mocker.patch("command_line_conflict.config.DEBUG", True)
    mocker.patch("command_line_conflict.scenes.game.log")

    game = MockGame()
    scene = GameScene(game)
    scene.fog_of_war = MagicMock()
    scene.cheats["reveal_map"] = False
    scene.rendering_system = MagicMock()
    scene.game_state.map = MagicMock()
    scene.ui_system = MagicMock()
    scene.chat_system = MagicMock()

    # Act
    scene.draw(MagicMock())

    # Assert
    # Fog of war SHOULD be drawn (active) even in debug mode, unless cheat is on
    scene.fog_of_war.draw.assert_called_once()


def test_reveal_map_cheat_disables_fog_of_war(mocker):
    # Arrange
    mocker.patch("command_line_conflict.config.DEBUG", False)
    mocker.patch("command_line_conflict.scenes.game.log")

    game = MockGame()
    scene = GameScene(game)
    scene.fog_of_war = MagicMock()
    scene.cheats["reveal_map"] = True
    scene.rendering_system = MagicMock()
    scene.game_state.map = MagicMock()
    scene.ui_system = MagicMock()
    scene.chat_system = MagicMock()

    # Act
    scene.draw(MagicMock())

    # Assert
    # Fog of war should NOT be drawn
    scene.fog_of_war.draw.assert_not_called()
