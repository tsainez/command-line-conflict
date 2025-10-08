from functools import wraps
from .. import config
from ..logger import log

def log_debug_only(func):
    """
    A decorator that ensures a log message is only processed when
    the game is in debug mode.
    """
    @wraps(func)
    def wrapper(message, *args, **kwargs):
        if config.DEBUG:
            func(message, *args, **kwargs)
    return wrapper

@log_debug_only
def debug_log(message, *args, **kwargs):
    """Logs a message at the INFO level, but only if DEBUG is enabled."""
    log.info(message, *args, **kwargs)