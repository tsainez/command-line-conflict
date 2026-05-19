from unittest.mock import MagicMock, patch

import pygame

from command_line_conflict.scenes.defeat import DefeatScene


@patch("pygame.mouse.set_cursor")
def test_defeat_scene_mousemotion_cursor(mock_set_cursor):
    """Test that moving the mouse in the defeat scene sets the cursor to a hand."""
    game_mock = MagicMock()
    scene = DefeatScene(game_mock)

    # Create a dummy MOUSEMOTION event
    event = MagicMock()
    event.type = pygame.MOUSEMOTION

    scene.handle_event(event)

    mock_set_cursor.assert_called_with(pygame.SYSTEM_CURSOR_HAND)


@patch("pygame.mouse.set_cursor")
def test_defeat_scene_escape_key(mock_set_cursor):
    """Test that pressing ESCAPE resets cursor and switches to the menu."""
    game_mock = MagicMock()
    scene = DefeatScene(game_mock)

    event = MagicMock()
    event.type = pygame.KEYDOWN
    event.key = pygame.K_ESCAPE

    scene.handle_event(event)

    mock_set_cursor.assert_called_with(pygame.SYSTEM_CURSOR_ARROW)
    game_mock.scene_manager.switch_to.assert_called_with("menu")


@patch("pygame.mouse.set_cursor")
def test_defeat_scene_mouse_click(mock_set_cursor):
    """Test that clicking resets cursor and switches to the menu."""
    game_mock = MagicMock()
    scene = DefeatScene(game_mock)

    event = MagicMock()
    event.type = pygame.MOUSEBUTTONDOWN

    scene.handle_event(event)

    mock_set_cursor.assert_called_with(pygame.SYSTEM_CURSOR_ARROW)
    game_mock.scene_manager.switch_to.assert_called_with("menu")
