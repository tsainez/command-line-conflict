import logging
import os
from unittest.mock import mock_open, patch

from command_line_conflict.logger import setup_logger


def test_setup_logger_default_level():
    """
    Tests that the logger is created with the default log level (INFO)
    when the LOG_LEVEL environment variable is not set.
    """
    logger = setup_logger()
    assert logger.level == logging.INFO


@patch.dict(os.environ, {"LOG_LEVEL": "DEBUG"})
def test_setup_logger_debug_level():
    """
    Tests that the logger is created with the DEBUG log level
    when the LOG_LEVEL environment variable is set to DEBUG.
    """
    logger = setup_logger()
    assert logger.level == logging.DEBUG


@patch("logging.FileHandler")
def test_setup_logger_file_handler_append_mode(mock_file_handler):
    """
    Tests that the file handler is created with append mode ('a').
    """
    setup_logger()
    mock_file_handler.assert_called_with("game.log", mode="a")
