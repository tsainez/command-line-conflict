import logging
import os
from unittest.mock import mock_open, patch

from command_line_conflict.logger import setup_logger


def test_setup_logger_default_level():
    """
    Tests that the logger is created with the default log level based on config.DEBUG
    when the LOG_LEVEL environment variable is not set.
    """
    with patch.dict(os.environ):
        if "LOG_LEVEL" in os.environ:
            del os.environ["LOG_LEVEL"]

        # Case 1: DEBUG is False -> INFO
        with patch("command_line_conflict.config.DEBUG", False):
            logger = setup_logger()
            assert logger.level == logging.INFO

        # Case 2: DEBUG is True -> DEBUG
        with patch("command_line_conflict.config.DEBUG", True):
            logger = setup_logger()
            assert logger.level == logging.DEBUG


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
