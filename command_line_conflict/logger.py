"""This module sets up the global logger for the application."""

import logging
import logging.handlers
import os
import sys

from . import config
from .utils.paths import get_user_data_dir


def setup_logger():
    """
    Sets up a logger that logs to both a file and the console.

    The log level is determined by the `LOG_LEVEL` environment variable.
    If the variable is not set, it defaults to DEBUG if config.DEBUG is True,
    else INFO.
    """
    # Create a logger
    logger = logging.getLogger("Command Line Conflict")
    default_level = "DEBUG" if config.DEBUG else "INFO"
    log_level = os.environ.get("LOG_LEVEL", default_level).upper()
    logger.setLevel(log_level)

    # Create a formatter
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # Create a file handler
    try:
        log_dir = get_user_data_dir()
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / "game.log"

        # Security: Rotate logs to prevent disk exhaustion (DoS)
        # Limit to 5MB, keep 1 backup
        file_handler = logging.handlers.RotatingFileHandler(str(log_file), maxBytes=5 * 1024 * 1024, backupCount=1)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except Exception as e:
        sys.stderr.write(f"Failed to setup log file: {e}\n")

    # Create a console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(console_handler)

    return logger


# Create a single logger instance to be used throughout the application
log = setup_logger()
