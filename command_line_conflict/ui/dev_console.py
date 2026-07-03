"""Developer Console UI."""

import pygame

from .. import config
from ..utils.profiler import profiler


class DeveloperConsole:
    """An overlay console to view developer and performance metrics."""

    def __init__(self, screen_width: int, screen_height: int, font: pygame.font.Font):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = font
        self.is_visible = False

        # Overlay properties
        self.width = screen_width
        self.height = int(screen_height * 0.3)  # Covers top 30% of screen
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.surface.fill((0, 0, 0, 200))  # Semi-transparent black

    def toggle(self) -> None:
        """Toggles the visibility of the console."""
        if getattr(config, "DEV_MODE", False):
            self.is_visible = not self.is_visible

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handles events for the console. Returns True if the event was consumed."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKQUOTE:  # Tilde key ~
                self.toggle()
                return True
        return False

    def draw(self, screen: pygame.Surface) -> None:
        """Draws the developer console if it is visible."""
        if not self.is_visible:
            return

        self.surface.fill((0, 0, 0, 200))
        stats = profiler.get_stats()

        lines = [
            "DEVELOPER CONSOLE",
            f"FPS: {stats['fps']:.1f} / {config.FPS}",
            f"Frame Drops: {stats['frame_drops']}",
            f"Memory Usage: {stats['memory_mb']:.2f} MB",
        ]

        y_offset = 10
        for line in lines:
            if self.font:
                text_surface = self.font.render(line, True, (0, 255, 0))  # Green text
                self.surface.blit(text_surface, (10, y_offset))
                y_offset += text_surface.get_height() + 5

        if self.font:
            hint_surface = self.font.render("Press ` to close", True, (150, 150, 150))
            self.surface.blit(hint_surface, (self.width - hint_surface.get_width() - 10, 10))

        screen.blit(self.surface, (0, 0))
