import pygame


class MenuHoverMixin:
    """Provides common hover effect logic for menu-based scenes."""

    def handle_hover_event(self, event):
        """Handles MOUSEMOTION events for menu options.

        Requires the instance to have `option_rects`, `selected_option`, and `sound_system`.

        Args:
            event: The pygame event.

        Returns:
            bool: True if the event was a MOUSEMOTION event and handled, False otherwise.
        """
        if event.type != pygame.MOUSEMOTION:
            return False

        hovered = False
        for rect, i in self.option_rects:
            if rect.collidepoint(event.pos):
                hovered = True
                if getattr(self, "selected_option", None) != i:
                    if hasattr(self, "sound_system"):
                        self.sound_system.play_sound("click_select")
                    self._on_selection_changed()
                self.selected_option = i

        if hovered:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        return True

    def _on_selection_changed(self):
        """Hook for subclasses when the selected option changes."""
        pass
