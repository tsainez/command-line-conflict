from unittest.mock import MagicMock, patch

import pytest

from command_line_conflict.ui.file_dialog import FileDialog


class TestFileDialogCursorBlinking:

    @pytest.fixture
    def mock_screen(self):
        return MagicMock()

    @pytest.fixture
    def mock_font(self):
        font = MagicMock()
        font.render.return_value = MagicMock()

        # Mock size to estimate width
        # Let's say each char is 10px wide
        def size(text):
            return (len(text) * 10, 20)

        font.size.side_effect = size
        return font

    @pytest.fixture
    def dialog(self, mock_screen, mock_font, tmp_path):
        initial_dir = str(tmp_path)
        with patch("pygame.time.get_ticks", return_value=0):
            dialog = FileDialog(mock_screen, mock_font, "Test Dialog", initial_dir, mode="load")
        return dialog

    @patch("pygame.draw.line")
    @patch("pygame.time.get_ticks")
    def test_cursor_blinking(self, mock_get_ticks, mock_draw_line, dialog, mock_screen):
        """Test that the cursor blinks over time."""

        # Initial state (t=0), initialized in fixture
        # Advance time to 0 (same as init)
        mock_get_ticks.return_value = 0
        dialog.draw()

        # Cursor should be visible initially
        # We expect a draw line call
        # The position depends on input_text which is empty, so x + 5
        # We need to verify that draw.line was called.
        assert mock_draw_line.called, "Cursor should be drawn initially"
        mock_draw_line.reset_mock()

        # Advance time to 200ms (still visible)
        mock_get_ticks.return_value = 200
        dialog.draw()
        assert mock_draw_line.called, "Cursor should still be visible at 200ms"
        mock_draw_line.reset_mock()

        # Advance time to 600ms (should toggle to invisible)
        mock_get_ticks.return_value = 600
        dialog.draw()
        assert not mock_draw_line.called, "Cursor should be invisible after 500ms"

        # Advance time to 1200ms (should toggle back to visible)
        # Previous toggle was at 600ms. 1200 - 600 = 600 > 500.
        mock_get_ticks.return_value = 1200
        dialog.draw()
        assert mock_draw_line.called, "Cursor should be visible again after 1000ms"

    @patch("pygame.draw.line")
    @patch("pygame.time.get_ticks")
    def test_cursor_position(self, mock_get_ticks, mock_draw_line, dialog, mock_screen):
        """Test that the cursor is drawn at the correct position."""
        mock_get_ticks.return_value = 0
        dialog.input_text = "ABC"  # 3 chars * 10px = 30px width

        dialog.draw()

        # Verify call args
        # pygame.draw.line(surface, color, start_pos, end_pos, width)
        # Expected X: input_rect.x + 5 + 30
        expected_x = dialog.input_rect.x + 5 + 30

        args, _ = mock_draw_line.call_args
        # args[0] is screen (mock_screen)
        # args[1] is color
        # args[2] is start_pos (x, y)
        start_pos = args[2]

        assert start_pos[0] == expected_x
