"""This module sets up the global logger for the application."""

import logging
import os
import sys


def setup_logger() -> logging.Logger:
    """Sets up a logger that logs to both a file and the console.

    The log level is determined by the `LOG_LEVEL` environment variable.
    If the variable is not set, it defaults to INFO.

    Returns:
        logging.Logger: The configured logger instance.
    """
    # Create a logger
    logger = logging.getLogger("Command Line Conflict")
    log_level = os.environ.get("LOG_LEVEL", "INFO").upper()
    logger.setLevel(log_level)

    # Create a formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Create a file handler
    file_handler = logging.FileHandler("game.log", mode="a")
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)

    # Create a console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


# Create a single logger instance to be used throughout the application
log = setup_logger()
