import pygame


class BaseEndScene:
    """Base class for endgame scenes to share common event handling."""

    def __init__(self, game):
        """Initializes the base end scene.

        Args:
            game: The main game object.
        """
        self.game = game
        self.font = game.font
        self.time = 0.0

    def handle_event(self, event):
        """Handles common events for the endgame scene.

        Args:
            event: The pygame event to handle.
        """
        if event.type == pygame.MOUSEMOTION:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        elif event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                self.game.scene_manager.switch_to("menu")
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.game.scene_manager.switch_to("menu")
