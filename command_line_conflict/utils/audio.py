import pygame

from ..logger import log


def init_mixer():
    """Initializes the pygame mixer if it hasn't been initialized already."""
    if not pygame.mixer.get_init():
        try:
            pygame.mixer.init()
            return True
        except pygame.error as e:
            log.error(f"Failed to initialize pygame mixer: {e}")
            return False
    return True
