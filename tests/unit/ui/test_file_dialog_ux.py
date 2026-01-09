from unittest.mock import MagicMock

import pytest

from command_line_conflict.ui.file_dialog import FileDialog


class TestFileDialogUX:

    @pytest.fixture
    def mock_screen(self):
        return MagicMock()

    @pytest.fixture
    def mock_font(self):
        font = MagicMock()
        font.render.return_value = MagicMock()

        # Mock size to estimate width for clipping tests
        # Let's say each char is 10px wide
        def size(text):
            return (len(text) * 10, 20)

        font.size.side_effect = size
        return font

    @pytest.fixture
    def empty_file_dialog(self, mock_screen, mock_font, tmp_path):
        initial_dir = str(tmp_path)
        # No files created

        dialog = FileDialog(mock_screen, mock_font, "Test Dialog", initial_dir, mode="load")

        # We need real rects for logic, but mocks are fine for collision tests if we don't use real mouse events here
        # But FileDialog creates real Rects in __init__.

        return dialog

    def test_draw_no_files_found(self, empty_file_dialog, mock_font):
        """Test that a message is displayed when no files are found."""
        empty_file_dialog.draw()

        # Check if "No files found" was rendered
        # We verify that font.render was called with something resembling "No files found"
        calls = [args[0] for args, _ in mock_font.render.call_args_list]
        assert "No files found" in calls

    def test_input_text_clipping(self, empty_file_dialog, mock_font, mock_screen):
        """Test that input text is clipped or handled when too long."""
        # Width is 600. Input rect width is width - 140 = 460.
        # If each char is 10px, 50 chars = 500px, which is > 460.

        long_text = "A" * 60  # 600px
        empty_file_dialog.input_text = long_text

        empty_file_dialog.draw()

        # Verify that set_clip was called with the input rect to constrain drawing
        # and then reset to None
        mock_screen.set_clip.assert_any_call(empty_file_dialog.input_rect)
        mock_screen.set_clip.assert_any_call(None)
