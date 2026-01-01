import os

import pygame

from command_line_conflict import config
from command_line_conflict.logger import log


class FileDialog:
    """A simple in-game file dialog for saving and loading files."""

    def __init__(
        self, screen, font, title, initial_dir, mode="load", extension=".json"
    ):  # pylint: disable=too-many-positional-arguments
        """Initializes the FileDialog.

        Args:
            screen: The pygame screen surface.
            font: The font to use for rendering text.
            title: The title of the dialog.
            initial_dir: The directory to browse.
            mode: "load" or "save".
            extension: The file extension to filter/append (e.g., ".json").
        """
        self.screen = screen
        self.font = font
        self.title = title
        self.initial_dir = initial_dir
        self.mode = mode
        self.extension = extension

        self.active = True
        self.selected_file = None
        self.input_text = ""
        self.files = []
        self.scroll_offset = 0
        self.max_visible_files = 10
        self.item_height = 30

        # Dimensions
        self.width = 600
        self.height = 400
        self.x = (config.SCREEN_WIDTH - self.width) // 2
        self.y = (config.SCREEN_HEIGHT - self.height) // 2

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.file_list_rect = pygame.Rect(self.x + 20, self.y + 60, self.width - 40, self.item_height * self.max_visible_files)
        self.input_rect = pygame.Rect(self.x + 20, self.y + self.height - 50, self.width - 140, 30)
        self.action_button_rect = pygame.Rect(self.x + self.width - 110, self.y + self.height - 50, 90, 30)
        self.close_button_rect = pygame.Rect(self.x + self.width - 30, self.y + 10, 20, 20)

        self.hovered_file_index = None
        self.hovered_element = None  # "close", "action", or None

        self.refresh_files()

    def refresh_files(self):
        """Refreshes the list of files in the current directory."""
        try:
            if not os.path.exists(self.initial_dir):
                os.makedirs(self.initial_dir)
            self.files = sorted([f for f in os.listdir(self.initial_dir) if f.endswith(self.extension)])
        except OSError as e:
            log.error(f"Error listing files: {e}")
            self.files = []

    def handle_event(self, event):
        """Handles events for the file dialog.

        Returns:
            str: The selected file path if confirmed, None otherwise.
        """
        if not self.active:
            return None

        if event.type == pygame.MOUSEMOTION:
            self.hovered_element = None
            self.hovered_file_index = None
            cursor_changed = False

            if self.close_button_rect.collidepoint(event.pos):
                self.hovered_element = "close"
                cursor_changed = True
            elif self.action_button_rect.collidepoint(event.pos):
                self.hovered_element = "action"
                cursor_changed = True
            elif self.file_list_rect.collidepoint(event.pos):
                idx = (event.pos[1] - self.file_list_rect.y) // self.item_height + self.scroll_offset
                if 0 <= idx < len(self.files):
                    self.hovered_file_index = idx
                    cursor_changed = True

            if cursor_changed:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                if self.close_button_rect.collidepoint(event.pos):
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    self.active = False
                    return None

                if self.file_list_rect.collidepoint(event.pos):
                    # Select file from list
                    idx = (event.pos[1] - self.file_list_rect.y) // self.item_height + self.scroll_offset
                    if 0 <= idx < len(self.files):
                        self.input_text = self.files[idx]
                        if self.mode == "load":
                            # Double click logic could go here, but for now single click selects
                            pass

                if self.action_button_rect.collidepoint(event.pos):
                    return self._confirm_selection()

            elif event.button == 4:  # Scroll up
                self.scroll_offset = max(0, self.scroll_offset - 1)
            elif event.button == 5:  # Scroll down
                self.scroll_offset = min(max(0, len(self.files) - self.max_visible_files), self.scroll_offset + 1)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                self.active = False
                return None
            if event.key == pygame.K_RETURN:
                return self._confirm_selection()
            if event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            else:
                # Add character to input
                if event.unicode.isprintable():
                    # Security: Limit input length to prevent DoS
                    max_len = getattr(config, "MAX_FILENAME_LENGTH", 64)
                    if len(self.input_text) < max_len:
                        self.input_text += event.unicode

        return None

    def _confirm_selection(self):
        """Confirms the current selection or input."""
        if not self.input_text:
            return None

        filename = self.input_text
        if not filename.endswith(self.extension):
            filename += self.extension

        # Security: Prevent path traversal
        filename = os.path.basename(filename)

        full_path = os.path.join(self.initial_dir, filename)
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        self.active = False
        return full_path

    def draw(self):
        """Draws the file dialog."""
        if not self.active:
            return

        # Draw background
        pygame.draw.rect(self.screen, (50, 50, 50), self.rect)
        pygame.draw.rect(self.screen, (200, 200, 200), self.rect, 2)  # Border

        # Draw Title
        title_surf = self.font.render(self.title, True, (255, 255, 255))
        self.screen.blit(title_surf, (self.x + 20, self.y + 20))

        # Draw Close Button
        close_color = (230, 80, 80) if self.hovered_element == "close" else (200, 50, 50)
        pygame.draw.rect(self.screen, close_color, self.close_button_rect)
        close_txt = self.font.render("X", True, (255, 255, 255))
        self.screen.blit(close_txt, (self.close_button_rect.x + 5, self.close_button_rect.y))

        # Draw File List Area
        pygame.draw.rect(self.screen, (30, 30, 30), self.file_list_rect)

        # Draw Files
        for i in range(self.max_visible_files):
            idx = i + self.scroll_offset
            if idx >= len(self.files):
                break

            f = self.files[idx]
            y_pos = self.file_list_rect.y + i * self.item_height
            item_rect = pygame.Rect(self.file_list_rect.x, y_pos, self.file_list_rect.width, self.item_height)

            # Highlight logic
            is_selected = f == self.input_text or (self.input_text.endswith(self.extension) and f == self.input_text)
            is_hovered = idx == self.hovered_file_index

            if is_selected:
                pygame.draw.rect(self.screen, (70, 70, 100), item_rect)
            elif is_hovered:
                pygame.draw.rect(self.screen, (50, 50, 60), item_rect)

            text_color = (255, 255, 255) if is_selected or is_hovered else (200, 200, 200)
            text_surf = self.font.render(f, True, text_color)
            self.screen.blit(text_surf, (self.file_list_rect.x + 5, y_pos + 5))

        # Draw Input Field
        pygame.draw.rect(self.screen, (255, 255, 255), self.input_rect)
        if self.input_text:
            input_surf = self.font.render(self.input_text, True, (0, 0, 0))
            input_surf_y = self.input_rect.y + 5
        else:
            input_surf = self.font.render("Enter a file name", True, (130, 130, 130))
            input_surf_y = self.input_rect.y + 5

        # Clip input text if too long? For now just render.
        self.screen.blit(input_surf, (self.input_rect.x + 5, input_surf_y))

        # Helper hint beneath the input for quick keyboard guidance.
        hint_text = "Enter to confirm, Esc to cancel, scroll to browse"
        hint_surf = self.font.render(hint_text, True, (170, 170, 170))
        self.screen.blit(hint_surf, (self.input_rect.x, self.input_rect.y + 32))

        # Draw Action Button
        action_enabled = bool(self.input_text)
        action_color = (70, 170, 70) if self.hovered_element == "action" and action_enabled else (50, 150, 50)
        if not action_enabled:
            action_color = (90, 90, 90)

        pygame.draw.rect(self.screen, action_color, self.action_button_rect)
        btn_text = "Save" if self.mode == "save" else "Load"
        btn_text_color = (255, 255, 255) if action_enabled else (200, 200, 200)
        btn_surf = self.font.render(btn_text, True, btn_text_color)
        self.screen.blit(btn_surf, (self.action_button_rect.x + 10, self.action_button_rect.y + 5))
