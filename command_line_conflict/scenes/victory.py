import math

from .base import BaseEndScene


class VictoryScene(BaseEndScene):
    """A scene to display when the player wins the game."""

    def update(self, dt):
        """Updates the victory scene.

        Args:
            dt: The time since the last frame.
        """
        self.time += dt

    def draw(self, screen):
        """Draws the victory scene.

        Args:
            screen: The pygame screen to draw on.
        """
        screen.fill((0, 0, 0))
        text = self.font.render("Victory!", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.game.screen.get_width() / 2, self.game.screen.get_height() / 2))
        screen.blit(text, text_rect)

        # Instructions to go back to menu
        pulse = (math.sin(self.time * 5) + 1) / 2
        color_val = 150 + int(105 * pulse)
        pulse_color = (color_val, color_val, color_val)
        instruction_text = self.font.render("Press Enter/Esc or Click to return to the menu", True, pulse_color)
        instruction_rect = instruction_text.get_rect(
            center=(
                self.game.screen.get_width() / 2,
                self.game.screen.get_height() / 2 + 50,
            )
        )
        screen.blit(instruction_text, instruction_rect)
