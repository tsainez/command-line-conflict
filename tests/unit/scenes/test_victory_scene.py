import pygame
from unittest.mock import MagicMock, patch
from command_line_conflict.scenes.victory import VictoryScene

@patch("pygame.mouse.set_cursor")
def test_victory_scene_mousemotion_cursor(mock_set_cursor):
    """Test that moving the mouse in the victory scene sets the cursor to a hand."""
    game_mock = MagicMock()
    scene = VictoryScene(game_mock)

    # Create a dummy MOUSEMOTION event
    event = MagicMock()
    event.type = pygame.MOUSEMOTION

    scene.handle_event(event)

    mock_set_cursor.assert_called_with(pygame.SYSTEM_CURSOR_HAND)

def test_victory_scene_escape_key():
    """Test that pressing ESCAPE switches to the menu."""
    game_mock = MagicMock()
    scene = VictoryScene(game_mock)

    event = MagicMock()
    event.type = pygame.KEYDOWN
    event.key = pygame.K_ESCAPE

    scene.handle_event(event)

    game_mock.scene_manager.switch_to.assert_called_with("menu")
