import os
import pygame
import pytest
from unittest.mock import MagicMock, patch
from command_line_conflict.ui.file_dialog import FileDialog

class TestFileDialog:
    @pytest.fixture
    def mock_screen(self):
        return MagicMock()

    @pytest.fixture
    def mock_font(self):
        font = MagicMock()
        font.render.return_value = MagicMock()
        font.render.return_value.get_height.return_value = 20
        return font

    @pytest.fixture
    def temp_dir(self, tmp_path):
        return str(tmp_path)

    def test_initialization(self, mock_screen, mock_font, temp_dir):
        rect = pygame.Rect(0, 0, 400, 300)
        dialog = FileDialog(rect, mock_font, temp_dir)

        assert dialog.rect == rect
        assert dialog.current_dir == os.path.abspath(temp_dir)
        assert dialog.mode == "save"
        # Should contain ".."
        assert len(dialog.files) == 1
        assert dialog.files[0]["name"] == ".."

    def test_refresh_files(self, mock_screen, mock_font, temp_dir):
        # Create some files
        os.makedirs(os.path.join(temp_dir, "subdir"))
        with open(os.path.join(temp_dir, "test.json"), "w") as f: f.write("{}")
        with open(os.path.join(temp_dir, "ignore.txt"), "w") as f: f.write("")

        rect = pygame.Rect(0, 0, 400, 300)
        dialog = FileDialog(rect, mock_font, temp_dir)

        files_names = [f["name"] for f in dialog.files]
        assert ".." in files_names
        assert "subdir" in files_names
        assert "test.json" in files_names
        assert "ignore.txt" not in files_names

    def test_file_selection(self, mock_screen, mock_font, temp_dir):
        with open(os.path.join(temp_dir, "test.json"), "w") as f: f.write("{}")

        rect = pygame.Rect(0, 0, 400, 300)
        dialog = FileDialog(rect, mock_font, temp_dir)

        # Determine click position for test.json
        # ".." is index 0, "test.json" is index 1
        # List starts at rect.y + 50 (header height)
        # Line height is 30

        dialog.list_area_rect = pygame.Rect(10, 50, 380, 200)
        click_y = 50 + 1 * 30 + 5
        click_x = 20

        event = MagicMock(type=pygame.MOUSEBUTTONDOWN, button=1, pos=(click_x, click_y))
        dialog.handle_event(event)

        assert dialog.selected_index == 1
        assert dialog.files[1]["name"] == "test.json"

        # In save mode, clicking fills input
        assert dialog.filename_input == "test.json"

    def test_directory_navigation(self, mock_screen, mock_font, temp_dir):
        subdir = os.path.join(temp_dir, "subdir")
        os.makedirs(subdir)

        rect = pygame.Rect(0, 0, 400, 300)
        dialog = FileDialog(rect, mock_font, temp_dir)

        # Click on "subdir" (index 1)
        dialog.list_area_rect = pygame.Rect(10, 50, 380, 200)
        click_y = 50 + 1 * 30 + 5
        click_x = 20

        event = MagicMock(type=pygame.MOUSEBUTTONDOWN, button=1, pos=(click_x, click_y))
        dialog.handle_event(event)

        assert dialog.current_dir == os.path.abspath(subdir)

        # Click on ".." (index 0 in subdir)
        click_y = 50 + 0 * 30 + 5
        event = MagicMock(type=pygame.MOUSEBUTTONDOWN, button=1, pos=(click_x, click_y))
        dialog.handle_event(event)

        assert dialog.current_dir == os.path.abspath(temp_dir)

    def test_save_confirmation(self, mock_screen, mock_font, temp_dir):
        rect = pygame.Rect(0, 0, 400, 300)
        mock_confirm = MagicMock()
        dialog = FileDialog(rect, mock_font, temp_dir, mode="save", on_confirm=mock_confirm)

        dialog.filename_input = "newmap"

        # Click Save Button
        # We need to set the confirm_btn_rect explicitly as it's calculated in init
        # Based on width 400, height 300
        # btn_width 80, btn_y = 260
        # cancel_x = 400 - 10 - 80 = 310
        # confirm_x = 310 - 10 - 80 = 220
        # rect: 220, 260, 80, 30

        event = MagicMock(type=pygame.MOUSEBUTTONDOWN, button=1, pos=(230, 270))
        dialog.handle_event(event)

        mock_confirm.assert_called_once()
        args = mock_confirm.call_args[0]
        assert args[0].endswith("newmap.json")

    def test_text_input(self, mock_screen, mock_font, temp_dir):
        rect = pygame.Rect(0, 0, 400, 300)
        dialog = FileDialog(rect, mock_font, temp_dir, mode="save")

        event = MagicMock(type=pygame.KEYDOWN, key=pygame.K_a, unicode="a")
        dialog.handle_event(event)
        assert dialog.filename_input == "a"

        event = MagicMock(type=pygame.KEYDOWN, key=pygame.K_b, unicode="b")
        dialog.handle_event(event)
        assert dialog.filename_input == "ab"

        event = MagicMock(type=pygame.KEYDOWN, key=pygame.K_BACKSPACE)
        dialog.handle_event(event)
        assert dialog.filename_input == "a"
