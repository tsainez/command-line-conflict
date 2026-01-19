import pytest
from unittest.mock import MagicMock, patch
from command_line_conflict.ui.file_dialog import FileDialog

def test_cursor_blinking_logic():
    screen = MagicMock()
    font = MagicMock()

    # Mock os.path.exists and os.listdir to avoid filesystem issues
    with patch("os.path.exists", return_value=True), \
         patch("os.listdir", return_value=[]):
        dialog = FileDialog(screen, font, "Test Dialog", ".", mode="save")

    # Initial state
    assert dialog.cursor_visible is True
    assert dialog.cursor_timer == 0.0

    # Update less than threshold (0.5s)
    dialog.update(0.4)
    assert dialog.cursor_visible is True
    assert dialog.cursor_timer == 0.4

    # Update to cross threshold
    dialog.update(0.1)  # Total 0.5 (actually >= 0.5 resets timer to 0)

    # After update(0.1), timer was 0.4 + 0.1 = 0.5.
    # Logic: if timer >= 0.5: visible = !visible; timer = 0.0
    assert dialog.cursor_visible is False
    assert dialog.cursor_timer == 0.0

    # Update again
    dialog.update(0.6)
    assert dialog.cursor_visible is True
    assert dialog.cursor_timer == 0.0

@patch("command_line_conflict.ui.file_dialog.pygame.draw.line")
def test_cursor_drawing(mock_draw_line):
    screen = MagicMock()
    font = MagicMock()

    with patch("os.path.exists", return_value=True), \
         patch("os.listdir", return_value=[]):
        dialog = FileDialog(screen, font, "Test Dialog", ".", mode="save")

    dialog.input_text = "test"

    # Mock font render
    mock_surf = MagicMock()
    mock_surf.get_width.return_value = 50
    font.render.return_value = mock_surf

    # 1. Cursor Visible
    dialog.cursor_visible = True
    dialog.draw()

    # Verify line drawn
    assert mock_draw_line.called

    # Check arguments: screen, color, start, end, width
    args, _ = mock_draw_line.call_args
    assert args[0] == screen
    assert args[1] == (0, 0, 0) # Black color

    # 2. Cursor Invisible
    mock_draw_line.reset_mock()
    dialog.cursor_visible = False
    dialog.draw()

    assert not mock_draw_line.called
