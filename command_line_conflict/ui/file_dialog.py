import os
import pygame
from command_line_conflict.logger import log

class FileDialog:
    """A modal file dialog for saving and loading files in-game."""

    def __init__(self, rect, font, initial_dir, mode="save", extension=".json", on_confirm=None, on_cancel=None):
        """Initializes the FileDialog.

        Args:
            rect: A pygame.Rect defining the dialog's position and size.
            font: The pygame.font.Font to use for rendering text.
            initial_dir: The directory to start in.
            mode: "save" or "load".
            extension: The file extension to filter by (e.g., ".json").
            on_confirm: Callback function(path) when a file is selected/saved.
            on_cancel: Callback function() when the dialog is cancelled.
        """
        self.rect = rect
        self.font = font
        self.current_dir = os.path.abspath(initial_dir)
        if not os.path.exists(self.current_dir):
            try:
                os.makedirs(self.current_dir)
            except OSError:
                self.current_dir = os.getcwd()

        self.mode = mode.lower()
        self.extension = extension
        self.on_confirm = on_confirm
        self.on_cancel = on_cancel

        self.files = []
        self.selected_index = -1
        self.scroll_offset = 0
        self.filename_input = ""

        # UI Layout Constants
        self.header_height = 50
        self.footer_height = 50
        self.line_height = 30
        self.list_area_rect = pygame.Rect(
            self.rect.x + 10,
            self.rect.y + self.header_height,
            self.rect.width - 20,
            self.rect.height - self.header_height - self.footer_height
        )
        self.items_visible = self.list_area_rect.height // self.line_height

        # Buttons
        btn_width = 80
        btn_height = 30
        btn_y = self.rect.bottom - 40

        self.cancel_btn_rect = pygame.Rect(self.rect.right - 10 - btn_width, btn_y, btn_width, btn_height)
        self.confirm_btn_rect = pygame.Rect(self.cancel_btn_rect.left - 10 - btn_width, btn_y, btn_width, btn_height)

        self.refresh_files()

    def refresh_files(self):
        """Refreshes the list of files in the current directory."""
        self.files = []
        self.selected_index = -1
        self.scroll_offset = 0

        try:
            # Add parent directory option
            self.files.append({"name": "..", "is_dir": True})

            entries = sorted(os.listdir(self.current_dir))
            for entry in entries:
                full_path = os.path.join(self.current_dir, entry)
                if os.path.isdir(full_path):
                    self.files.append({"name": entry, "is_dir": True})
                elif entry.endswith(self.extension) or self.extension == "*":
                    self.files.append({"name": entry, "is_dir": False})
        except OSError as e:
            log.error(f"Error listing directory {self.current_dir}: {e}")

    def handle_event(self, event):
        """Handles pygame events passed to the dialog."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Left click
                self._handle_click(event.pos)
            elif event.button == 4: # Scroll Up
                self.scroll_offset = max(0, self.scroll_offset - 1)
            elif event.button == 5: # Scroll Down
                max_scroll = max(0, len(self.files) - self.items_visible)
                self.scroll_offset = min(max_scroll, self.scroll_offset + 1)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if self.on_cancel: self.on_cancel()
            elif event.key == pygame.K_RETURN:
                self._confirm()
            elif self.mode == "save":
                self._handle_text_input(event)

    def _handle_text_input(self, event):
        if event.key == pygame.K_BACKSPACE:
            self.filename_input = self.filename_input[:-1]
        elif event.unicode.isprintable():
            # Basic validation
            if len(self.filename_input) < 50:
                self.filename_input += event.unicode

    def _handle_click(self, pos):
        if not self.rect.collidepoint(pos):
            # Clicking outside doesn't close strictly, but could.
            # For now, ignore.
            return

        # Check Buttons
        if self.confirm_btn_rect.collidepoint(pos):
            self._confirm()
            return
        if self.cancel_btn_rect.collidepoint(pos):
            if self.on_cancel: self.on_cancel()
            return

        # Check List Items
        if self.list_area_rect.collidepoint(pos):
            rel_y = pos[1] - self.list_area_rect.y
            clicked_row = rel_y // self.line_height
            clicked_index = self.scroll_offset + clicked_row

            if 0 <= clicked_index < len(self.files):
                item = self.files[clicked_index]
                if item["is_dir"]:
                    # Navigate
                    new_dir = os.path.normpath(os.path.join(self.current_dir, item["name"]))
                    if os.path.isdir(new_dir):
                        self.current_dir = new_dir
                        self.refresh_files()
                else:
                    self.selected_index = clicked_index
                    if self.mode == "save":
                         self.filename_input = item["name"]

    def _confirm(self):
        filename = None
        if self.mode == "save":
            filename = self.filename_input.strip()
            if filename and not filename.endswith(self.extension):
                filename += self.extension
        elif self.mode == "load":
            if 0 <= self.selected_index < len(self.files):
                item = self.files[self.selected_index]
                if not item["is_dir"]:
                    filename = item["name"]

        if filename:
            path = os.path.join(self.current_dir, filename)
            if self.on_confirm: self.on_confirm(path)

    def draw(self, screen):
        """Draws the dialog."""
        # Draw Panel Background
        pygame.draw.rect(screen, (30, 30, 30), self.rect)
        pygame.draw.rect(screen, (100, 100, 100), self.rect, 2)

        # Header
        title = f"{self.mode.capitalize()} Map"
        title_surf = self.font.render(title, True, (255, 255, 255))
        screen.blit(title_surf, (self.rect.x + 10, self.rect.y + 10))

        # Path (Truncate head if too long)
        path_str = self.current_dir
        if len(path_str) > 50:
            path_str = "..." + path_str[-47:]
        path_surf = self.font.render(path_str, True, (180, 180, 180))
        screen.blit(path_surf, (self.rect.x + 10, self.rect.y + 35)) # Small font? reusing main font

        # List Area Background
        pygame.draw.rect(screen, (20, 20, 20), self.list_area_rect)
        pygame.draw.rect(screen, (60, 60, 60), self.list_area_rect, 1)

        # Draw Files
        clip_rect = self.list_area_rect
        old_clip = screen.get_clip()
        screen.set_clip(clip_rect)

        for i in range(self.items_visible + 1): # +1 to cover partials if any
            idx = self.scroll_offset + i
            if idx >= len(self.files): break

            item = self.files[idx]
            y_pos = self.list_area_rect.y + i * self.line_height

            # Highlight selection
            if idx == self.selected_index:
                pygame.draw.rect(screen, (50, 50, 100), (self.list_area_rect.x, y_pos, self.list_area_rect.width, self.line_height))

            color = (255, 255, 100) if item["is_dir"] else (255, 255, 255)
            prefix = "[DIR] " if item["is_dir"] else ""
            text = f"{prefix}{item['name']}"

            # Simple render
            surf = self.font.render(text, True, color)
            # Vertical center text in line
            text_y = y_pos + (self.line_height - surf.get_height()) // 2
            screen.blit(surf, (self.list_area_rect.x + 5, text_y))

        screen.set_clip(old_clip)

        # Input Box (Save mode)
        input_y = self.rect.bottom - 40
        input_width = self.rect.width - 200 # Leave space for buttons
        input_rect = pygame.Rect(self.rect.x + 10, input_y, input_width, 30)

        if self.mode == "save":
            pygame.draw.rect(screen, (0, 0, 0), input_rect)
            pygame.draw.rect(screen, (100, 100, 100), input_rect, 1)

            txt = self.filename_input
            if len(txt) > 30: txt = "..." + txt[-27:]
            surf = self.font.render(txt + "_", True, (255, 255, 255))
            screen.blit(surf, (input_rect.x + 5, input_rect.y + (30 - surf.get_height())//2))

        # Buttons
        # Confirm
        pygame.draw.rect(screen, (50, 150, 50), self.confirm_btn_rect)
        pygame.draw.rect(screen, (255, 255, 255), self.confirm_btn_rect, 1)
        label = "Save" if self.mode == "save" else "Load"
        lbl_surf = self.font.render(label, True, (255, 255, 255))
        lbl_rect = lbl_surf.get_rect(center=self.confirm_btn_rect.center)
        screen.blit(lbl_surf, lbl_rect)

        # Cancel
        pygame.draw.rect(screen, (150, 50, 50), self.cancel_btn_rect)
        pygame.draw.rect(screen, (255, 255, 255), self.cancel_btn_rect, 1)
        lbl_surf = self.font.render("Cancel", True, (255, 255, 255))
        lbl_rect = lbl_surf.get_rect(center=self.cancel_btn_rect.center)
        screen.blit(lbl_surf, lbl_rect)
