import logging
import sys

def setup_logger():
    """
    Sets up a logger that logs to both a file and the console.
    """
    # Create a logger
    logger = logging.getLogger('Command Line Conflict')
    logger.setLevel(logging.DEBUG)  # Set the lowest level to capture all messages

    # Create a formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Create a file handler
    file_handler = logging.FileHandler('game.log', mode='w')
    file_handler.setLevel(logging.DEBUG)  # Log all debug messages to the file
    file_handler.setFormatter(formatter)

    # Create a console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)  # Only log INFO and above to the console
    console_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

# Create a single logger instance to be used throughout the application
log = setup_logger()
