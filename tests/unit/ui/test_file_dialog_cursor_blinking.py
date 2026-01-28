import os
import math
from unittest.mock import MagicMock, patch

import pygame
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
        # Mock surface dimensions for cursor positioning
        font.render.return_value.get_width.return_value = 50
        font.render.return_value.get_height.return_value = 20
        return font

    @pytest.fixture
    def file_dialog(self, mock_screen, mock_font, tmp_path):
        initial_dir = str(tmp_path)
        return FileDialog(mock_screen, mock_font, "Test Dialog", initial_dir, mode="load")

    def test_cursor_initialization(self, file_dialog):
        assert file_dialog.time == 0.0

    def test_cursor_update(self, file_dialog):
        file_dialog.update(0.1)
        assert file_dialog.time == 0.1

        file_dialog.update(0.5)
        assert file_dialog.time == 0.6

    def test_cursor_inactive_update(self, file_dialog):
        file_dialog.active = False
        file_dialog.update(0.1)
        # Should not update time if inactive?
        # Actually my implementation updates time only if active
        # Let's verify implementation logic: "if self.active: self.time += dt"
        assert file_dialog.time == 0.0

    def test_cursor_draw_blinking(self, file_dialog):
        # Time = 0.0 -> sin(0) = 0. Not drawn (condition > 0)
        # Wait, usually sin(0) is 0. So strict > 0 means not drawn at exact 0.
        # Let's advance time to where sin is positive.
        # sin(time * 8) > 0.
        # time=0.1 -> 0.8 rad (~45 deg) -> positive.

        file_dialog.time = 0.1

        with patch("pygame.draw.line") as mock_line:
            file_dialog.draw()
            # Expect line to be drawn
            mock_line.assert_called()

    def test_cursor_draw_blinking_off(self, file_dialog):
        # time such that sin(time*8) < 0
        # pi = 3.14. pi/8 = 0.39.
        # let's try time = 0.5 (4.0 rad) -> sin(4) is negative (-0.75)

        file_dialog.time = 0.5

        with patch("pygame.draw.line") as mock_line:
            file_dialog.draw()
            # Expect line NOT to be drawn
            mock_line.assert_not_called()
