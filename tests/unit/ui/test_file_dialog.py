import os
from unittest.mock import MagicMock

import pygame
import pytest

from command_line_conflict.ui.file_dialog import FileDialog


class TestFileDialog:

    @pytest.fixture
    def mock_screen(self):
        return MagicMock()

    @pytest.fixture
    def mock_font(self):
        font = MagicMock()
        font.render.return_value = MagicMock()
        return font

    @pytest.fixture
    def file_dialog(self, mock_screen, mock_font, tmp_path):
        initial_dir = str(tmp_path)
        # Create some dummy files
        with open(os.path.join(initial_dir, "map1.json"), "w") as f:
            f.write("{}")
        with open(os.path.join(initial_dir, "map2.json"), "w") as f:
            f.write("{}")
        with open(os.path.join(initial_dir, "other.txt"), "w") as f:
            f.write("")

        dialog = FileDialog(mock_screen, mock_font, "Test Dialog", initial_dir, mode="load")

        # Replace rects with mocks that we can control
        dialog.close_button_rect = MagicMock()
        dialog.close_button_rect.collidepoint.return_value = False

        dialog.file_list_rect = MagicMock()
        dialog.file_list_rect.collidepoint.return_value = False
        dialog.file_list_rect.y = 100

        dialog.action_button_rect = MagicMock()
        dialog.action_button_rect.collidepoint.return_value = False

        dialog.input_rect = MagicMock()
        dialog.input_rect.collidepoint.return_value = False

        return dialog

    def test_initialization(self, file_dialog):
        assert file_dialog.active is True
        assert len(file_dialog.files) == 2
        assert "map1.json" in file_dialog.files
        assert "map2.json" in file_dialog.files
        assert "other.txt" not in file_dialog.files

    def test_selection(self, file_dialog):
        # Simulate click on first file
        file_dialog.file_list_rect.collidepoint.return_value = True

        # Mock event
        event = MagicMock()
        event.type = pygame.MOUSEBUTTONDOWN
        event.button = 1
        event.pos = (150, 105)  # Just inside first item

        # We need to rely on the actual implementation of idx calculation
        # idx = (event.pos[1] - self.file_list_rect.y) // self.item_height + self.scroll_offset
        # 105 - 100 = 5. 5 // 30 = 0. So index 0.

        file_dialog.handle_event(event)

        assert file_dialog.input_text == "map1.json"

    def test_close_button(self, file_dialog):
        event = MagicMock()
        event.type = pygame.MOUSEBUTTONDOWN
        event.button = 1
        event.pos = (0, 0)

        file_dialog.close_button_rect.collidepoint.return_value = True

        file_dialog.handle_event(event)

        assert file_dialog.active is False

    def test_confirm_selection(self, file_dialog):
        file_dialog.input_text = "map1.json"

        event = MagicMock()
        event.type = pygame.MOUSEBUTTONDOWN
        event.button = 1
        event.pos = (0, 0)

        file_dialog.action_button_rect.collidepoint.return_value = True

        result = file_dialog.handle_event(event)

        assert result is not None
        assert result.endswith("map1.json")
        assert file_dialog.active is False

    def test_keyboard_input(self, file_dialog):
        event = MagicMock()
        event.type = pygame.KEYDOWN
        event.key = pygame.K_a
        event.unicode = "a"

        file_dialog.handle_event(event)
        assert file_dialog.input_text == "a"

        event.key = pygame.K_BACKSPACE
        file_dialog.handle_event(event)
        assert file_dialog.input_text == ""

    def test_escape_closes(self, file_dialog):
        event = MagicMock()
        event.type = pygame.KEYDOWN
        event.key = pygame.K_ESCAPE

        file_dialog.handle_event(event)
        assert file_dialog.active is False

    def test_hover_states(self, file_dialog):
        # Move over close button
        event = MagicMock()
        event.type = pygame.MOUSEMOTION
        event.pos = (0, 0)
        file_dialog.close_button_rect.collidepoint.return_value = True
        file_dialog.action_button_rect.collidepoint.return_value = False
        file_dialog.file_list_rect.collidepoint.return_value = False

        file_dialog.handle_event(event)
        assert file_dialog.hovered_element == "close"
        assert file_dialog.hovered_file_index is None

        # Move over action button
        event.pos = (100, 100)
        file_dialog.close_button_rect.collidepoint.return_value = False
        file_dialog.action_button_rect.collidepoint.return_value = True

        file_dialog.handle_event(event)
        assert file_dialog.hovered_element == "action"
        assert file_dialog.hovered_file_index is None

        # Move over file list
        event.pos = (150, 105)  # Index 0
        file_dialog.action_button_rect.collidepoint.return_value = False
        file_dialog.file_list_rect.collidepoint.return_value = True

        file_dialog.handle_event(event)
        assert file_dialog.hovered_element is None
        assert file_dialog.hovered_file_index == 0

        # Move outside
        event.pos = (500, 500)
        file_dialog.file_list_rect.collidepoint.return_value = False

        file_dialog.handle_event(event)
        assert file_dialog.hovered_element is None
        assert file_dialog.hovered_file_index is None

    def test_empty_state_rendering(self, file_dialog):
        """Test rendering when no files are available."""
        file_dialog.files = []
        # Calling draw should not crash
        try:
            file_dialog.draw()
        except Exception as e:
            pytest.fail(f"draw() raised exception with empty files: {e}")

    def test_scrollbar_rendering(self, file_dialog):
        """Test rendering when files exceed visible area."""
        # Create enough files to trigger scrollbar (max_visible_files is 10)
        file_dialog.files = [f"file{i}.json" for i in range(20)]
        file_dialog.scroll_offset = 5

        try:
            file_dialog.draw()
        except Exception as e:
            pytest.fail(f"draw() raised exception with scrollbar: {e}")
