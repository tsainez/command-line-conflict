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
        if "LOG_LEVEL" in os.environ:
            del os.environ["LOG_LEVEL"]

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
@patch("command_line_conflict.logger.logging.handlers.RotatingFileHandler")
@patch("command_line_conflict.logger.get_user_data_dir")
def test_setup_logger_file_handler_secure(
    mock_get_user_data, mock_rotating_handler, mock_get_logger
):
    """
    Tests that the logger uses RotatingFileHandler in the user data directory.
    """
    mock_logger = MagicMock()
    mock_get_logger.return_value = mock_logger

    mock_path = MagicMock()
    mock_get_user_data.return_value = mock_path
    # Mock the / operator for Path
    mock_log_file_path = MagicMock()
    mock_log_file_path.__str__.return_value = "/mock/path/game.log"
    mock_path.__truediv__.return_value = mock_log_file_path

    setup_logger()

    # Verify directory creation
    mock_path.mkdir.assert_called_with(parents=True, exist_ok=True)

    # Verify secure handler usage
    mock_rotating_handler.assert_called_with(
        "/mock/path/game.log", maxBytes=5 * 1024 * 1024, backupCount=1
    )
