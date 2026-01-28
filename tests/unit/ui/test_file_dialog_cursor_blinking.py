from unittest.mock import MagicMock, patch

import pygame

from command_line_conflict.ui.file_dialog import FileDialog


def test_cursor_blinking():
    # Mock dependencies
    screen = MagicMock()
    font = MagicMock()
    # Mock font size and height
    font.size.return_value = (100, 20)
    font.get_height.return_value = 20

    # Initialize FileDialog
    # We mock os.path.exists and os.listdir because __init__ calls refresh_files
    with patch("os.path.exists", return_value=True), patch("os.listdir", return_value=[]):
        dialog = FileDialog(screen, font, "Test", "test_dir")

    # Initial state: cursor visible
    assert dialog.cursor_visible is True
    assert dialog.cursor_timer == 0.0

    # Update less than threshold
    dialog.update(0.1)
    assert dialog.cursor_visible is True
    assert dialog.cursor_timer == 0.1

    # Update to cross threshold (0.5s)
    # 0.1 + 0.4 = 0.5
    dialog.update(0.4)
    assert dialog.cursor_visible is False
    assert dialog.cursor_timer == 0.0

    # Update again to toggle back
    dialog.update(0.5)
    assert dialog.cursor_visible is True
    assert dialog.cursor_timer == 0.0

    # Update to nearly cross threshold
    dialog.update(0.49)
    assert dialog.cursor_visible is True
    assert dialog.cursor_timer == 0.49

    # Cross it
    dialog.update(0.02)
    assert dialog.cursor_visible is False
    assert dialog.cursor_timer == 0.0
