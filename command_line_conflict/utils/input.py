import pygame


def set_cursor(cursor_type):
    """Sets the mouse cursor."""
    try:
        pygame.mouse.set_cursor(cursor_type)
    except pygame.error:
        pass
