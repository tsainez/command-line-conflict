import os
from unittest.mock import MagicMock, patch

from command_line_conflict.logger import setup_logger


@patch("command_line_conflict.logger.logging.getLogger")
def test_setup_logger_default_level(mock_get_logger):
    """
    Tests that the logger is created with the default log level based on config.DEBUG
    when the LOG_LEVEL environment variable is not set.
    """
    mock_logger = MagicMock()
    mock_get_logger.return_value = mock_logger

    with patch.dict(os.environ):
        os.environ.pop("LOG_LEVEL", None)

        # Case 1: DEBUG is False -> INFO
        with patch("command_line_conflict.config.DEBUG", False):
            setup_logger()
            mock_logger.setLevel.assert_called_with("INFO")

        # Case 2: DEBUG is True -> DEBUG
        with patch("command_line_conflict.config.DEBUG", True):
            setup_logger()
            mock_logger.setLevel.assert_called_with("DEBUG")


@patch("command_line_conflict.logger.logging.getLogger")
@patch.dict(os.environ, {"LOG_LEVEL": "DEBUG"})
def test_setup_logger_debug_level(mock_get_logger):
    """
    Tests that the logger is created with the DEBUG log level
    when the LOG_LEVEL environment variable is set to DEBUG.
    """
    mock_logger = MagicMock()
    mock_get_logger.return_value = mock_logger

    setup_logger()
    mock_logger.setLevel.assert_called_with("DEBUG")


@patch("command_line_conflict.logger.logging.getLogger")
@patch("command_line_conflict.logger.logging.FileHandler")
def test_setup_logger_file_handler_append_mode(mock_file_handler, mock_get_logger):
    """
    Tests that the file handler is created with append mode ('a').
    """
    mock_logger = MagicMock()
    mock_get_logger.return_value = mock_logger

    setup_logger()
    mock_file_handler.assert_called_with("game.log", mode="a")
