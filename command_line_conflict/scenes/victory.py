import pygame


class VictoryScene:
    """A scene to display when the player wins the game."""

    def __init__(self, game):
        """Initializes the VictoryScene.

        Args:
            game: The main game object.
        """
        self.game = game
        self.font = game.font

    def handle_event(self, event):
        """Handles events for the victory scene.

        Args:
            event: The pygame event to handle.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.game.scene_manager.switch_to("menu")

    def update(self, dt):
        """Updates the victory scene.

        Args:
            dt: The time since the last frame.
        """

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
        instruction_text = self.font.render("Press Enter to return to the menu", True, (255, 255, 255))
        instruction_rect = instruction_text.get_rect(
            center=(
                self.game.screen.get_width() / 2,
                self.game.screen.get_height() / 2 + 50,
            )
        )
        screen.blit(instruction_text, instruction_rect)
