import pygame


class MenuHoverMixin:
    """A mixin for scenes that have selectable menu options."""

    def handle_mouse_hover(self, pos):
        """Handles mouse hover effects for menu items.

        Args:
            pos: The (x, y) coordinates of the mouse.

        Returns:
            bool: True if the selected option changed, False otherwise.
        """
        hovered = False
        changed = False

        for rect, i in self.option_rects:
            if rect.collidepoint(pos):
                hovered = True
                if getattr(self, "selected_option", None) != i:
                    sound_system = getattr(self, "sound_system", None)
                    if sound_system:
                        sound_system.play_sound("click_select")

                    if hasattr(self, "quit_confirm"):
                        self.quit_confirm = False

                    changed = True
                self.selected_option = i

        if hovered:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        return changed
