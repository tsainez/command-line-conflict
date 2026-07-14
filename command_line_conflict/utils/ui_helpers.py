import math
from typing import Tuple

import pygame


def draw_title_and_get_pulse(
    screen: pygame.Surface,
    title_text: pygame.Surface,
    time: float,
    center_y: int = 100,
) -> Tuple[int, int, int]:
    """Draws a title text surface centered on the screen and returns a pulse color.

    This helper encapsulates common title rendering and pulse calculation logic used
    across various menu and setting screens.

    Args:
        screen: The pygame screen surface to draw on.
        title_text: The pre-rendered title text surface.
        time: The current scene time used for the pulse calculation.
        center_y: The y-coordinate to center the title on.

    Returns:
        A tuple representing the calculated RGB pulse color.
    """
    title_rect = title_text.get_rect(center=(screen.get_width() / 2, center_y))
    screen.blit(title_text, title_rect)

    # Pulse calculation: varies between 0 and 1
    pulse = (math.sin(time * 5) + 1) / 2
    # Interpolate between dim yellow (150, 150, 0) and bright yellow (255, 255, 0)
    yellow_val = 150 + int(105 * pulse)
    return (yellow_val, yellow_val, 0)
