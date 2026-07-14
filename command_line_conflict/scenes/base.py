import math
from typing import Tuple

import pygame


class BaseScene:
    """Base class for scenes providing common rendering logic."""

    def _draw_pulsing_title(self, screen: pygame.Surface, title: str, time: float) -> Tuple[int, int, int]:
        """Draws the scene title and calculates a pulsing color for options.

        Args:
            screen: The pygame screen surface to draw on.
            title: The text for the scene title.
            time: Current scene time, used to calculate the pulse.

        Returns:
            The calculated pulsing RGB color tuple (R, G, B).
        """
        title_text = self._get_text_surface(title, (255, 255, 255), "title")  # type: ignore
        title_rect = title_text.get_rect(center=(self.game.screen.get_width() / 2, 100))  # type: ignore
        screen.blit(title_text, title_rect)

        # Pulse calculation: varies between 0 and 1
        pulse = (math.sin(time * 5) + 1) / 2
        # Interpolate between dim yellow (150, 150, 0) and bright yellow (255, 255, 0)
        yellow_val = 150 + int(105 * pulse)
        return (yellow_val, yellow_val, 0)
