from unittest.mock import MagicMock
import pytest
from command_line_conflict.ui.file_dialog import FileDialog

class TestFileDialogCursor:
    @pytest.fixture
    def dialog(self):
        screen = MagicMock()
        font = MagicMock()
        font.size.return_value = (100, 20) # Mock text size
        initial_dir = "/tmp"
        return FileDialog(screen, font, "Test", initial_dir)

    def test_cursor_initialization(self, dialog):
        """Test that cursor attributes are initialized."""
        # These attributes will be added
        assert hasattr(dialog, "cursor_visible")
        assert hasattr(dialog, "cursor_timer")
        assert dialog.cursor_visible is True # Should start visible

    def test_cursor_blinking(self, dialog):
        """Test that the cursor blinks over time."""
        # Assume BLINK_INTERVAL is 0.5
        dialog.cursor_timer = 0
        dialog.cursor_visible = True

        # Advance time by 0.4s (should still be visible)
        dialog.update(0.4)
        assert dialog.cursor_visible is True

        # Advance time by 0.2s (total 0.6s -> should toggle)
        dialog.update(0.2)
        assert dialog.cursor_visible is False

        # Advance time by 0.5s (should toggle back)
        dialog.update(0.5)
        assert dialog.cursor_visible is True
