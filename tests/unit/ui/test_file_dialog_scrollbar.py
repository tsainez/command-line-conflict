from unittest.mock import MagicMock, patch

import pytest

# We need to ensure pygame is mocked before importing FileDialog
# This is handled by conftest.py, but we need to be careful with imports


class TestFileDialogScrollbar:
    @pytest.fixture
    def mock_screen(self):
        return MagicMock()

    @pytest.fixture
    def mock_font(self):
        font = MagicMock()
        # Mock render to return a surface with get_rect
        surface = MagicMock()
        surface.get_rect.return_value = MagicMock(width=100, height=20)
        font.render.return_value = surface
        return font

    @pytest.fixture
    def file_dialog(self, mock_screen, mock_font, mocker):
        # Patch os.path.exists and os.listdir to control initialization
        with patch("os.path.exists", return_value=True), patch("os.listdir", return_value=[]):
            from command_line_conflict.ui.file_dialog import FileDialog

            dialog = FileDialog(mock_screen, mock_font, "Test Dialog", "/tmp")

            # Setup necessary attributes for drawing
            # We use a distinct rect to avoid confusion with other UI elements
            dialog.file_list_rect = MagicMock()
            dialog.file_list_rect.x = 100
            dialog.file_list_rect.y = 100
            dialog.file_list_rect.height = 300
            dialog.file_list_rect.width = 200
            dialog.file_list_rect.right = 300
            dialog.file_list_rect.top = 100
            dialog.file_list_rect.bottom = 400

            # Move buttons far away (negative coordinates) to avoid interference in tests
            dialog.close_button_rect = MagicMock()
            dialog.close_button_rect.x = -1000
            dialog.action_button_rect = MagicMock()
            dialog.action_button_rect.x = -1000

            return dialog

    def test_draw_scrollbar_when_files_overflow(self, file_dialog):
        """Test that a scrollbar is drawn when there are more files than can be displayed."""
        # Setup state with many files
        file_dialog.files = [f"file_{i}.json" for i in range(20)]
        file_dialog.max_visible_files = 10
        file_dialog.scroll_offset = 5

        # Mock pygame.draw.rect to capture calls
        with patch("pygame.draw.rect") as mock_draw_rect:
            file_dialog.draw()

            # We look for the scrollbar thumb
            # It should be on the right side of file_list_rect
            # Allow some tolerance
            min_x = file_dialog.file_list_rect.right - 15
            max_x = file_dialog.file_list_rect.right + 5

            scrollbar_calls = []
            for call in mock_draw_rect.call_args_list:
                args = call[0]
                if len(args) >= 3:
                    rect = args[2]
                    # Check if rect is in the expected scrollbar area
                    if hasattr(rect, "x") and min_x <= rect.x <= max_x:
                        scrollbar_calls.append(call)

            assert len(scrollbar_calls) >= 1, "Scrollbar thumb should be drawn"

    def test_no_scrollbar_when_files_fit(self, file_dialog):
        """Test that NO scrollbar is drawn when files fit in the view."""
        file_dialog.files = [f"file_{i}.json" for i in range(5)]
        file_dialog.max_visible_files = 10

        with patch("pygame.draw.rect") as mock_draw_rect:
            file_dialog.draw()

            min_x = file_dialog.file_list_rect.right - 15
            max_x = file_dialog.file_list_rect.right + 5

            scrollbar_calls = []
            for call in mock_draw_rect.call_args_list:
                args = call[0]
                if len(args) >= 3:
                    rect = args[2]
                    if hasattr(rect, "x") and min_x <= rect.x <= max_x:
                        scrollbar_calls.append(call)

            assert len(scrollbar_calls) == 0, "Scrollbar should not be drawn when files fit"
