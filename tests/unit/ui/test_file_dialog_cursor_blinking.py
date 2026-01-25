from unittest.mock import MagicMock
import pytest
from command_line_conflict.ui.file_dialog import FileDialog

class TestFileDialogCursor:
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
        return FileDialog(mock_screen, mock_font, "Test", str(tmp_path))

    def test_initialization_time(self, file_dialog):
        """Verify time initializes to 0.0."""
        assert file_dialog.time == 0.0

    def test_update_increments_time(self, file_dialog):
        """Verify update(dt) increments time correctly."""
        file_dialog.update(0.5)
        assert file_dialog.time == 0.5
        file_dialog.update(0.3)
        assert file_dialog.time == 0.8
