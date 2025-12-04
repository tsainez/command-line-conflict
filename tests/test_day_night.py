import os
import pytest
from unittest.mock import MagicMock, patch

# In conftest.py, pygame.Surface is mocked as MagicMock.
# So we can't create real Surfaces inside tests unless we patch it back or handle it.
# However, for our test, we just want to verify logic.
# The error happens because pygame.transform.scale expects a REAL Surface (C object) if pygame itself is real,
# but conftest.py mocks pygame.Surface to be MagicMock.
# BUT, conftest.py does `mocker.patch("pygame.Surface", new=mocker.MagicMock())`.
# If `pygame` is the real module, `pygame.transform.scale` is the real function.
# Real function `scale` checks type of argument. It sees MagicMock, which is not Surface.
# We need to mock `pygame.transform.scale` too.

import pygame
from command_line_conflict.scenes.game import GameScene
from command_line_conflict.game_state import GameState
from command_line_conflict import config

class MockGame:
    def __init__(self):
        self.screen = MagicMock()
        self.screen.get_size.return_value = (800, 600)
        self.font = MagicMock()
        # font.render returns a mock surface
        self.font.render.return_value = MagicMock()
        self.scene_manager = MagicMock()
        self.music_manager = MagicMock()

def test_day_night_cycle_update():
    game = MockGame()

    # We must patch factories.create_chassis because GameScene calls it in init
    # We also need to patch RenderingSystem or mock out pygame.transform.scale

    with patch('command_line_conflict.factories.create_chassis'), \
         patch('pygame.transform.scale'):

        scene = GameScene(game)

        # Verify initial state
        assert scene.game_state.time_elapsed == 0.0
        assert scene.game_state.day_night_cycle_duration == 300

        # Update and check time_elapsed
        dt = 1.0
        scene.update(dt)
        assert scene.game_state.time_elapsed == 1.0

        # Check wrap around
        scene.game_state.time_elapsed = 299.5
        scene.update(1.0) # Should go to 300.5 -> 0.5
        assert scene.game_state.time_elapsed == 0.5

def test_day_night_cycle_overlay_logic():
    # Since we can't easily test visual output with mocks without extensive setup,
    # we will rely on checking if blit is called with correct parameters.

    game = MockGame()

    with patch('command_line_conflict.factories.create_chassis'), \
         patch('pygame.transform.scale'), \
         patch('pygame.draw.line'), \
         patch('pygame.Surface') as mock_surface_cls:

        # Mock Surface for __init__ creation
        mock_overlay = MagicMock()
        mock_overlay.get_size.return_value = (800, 600)
        mock_surface_cls.return_value = mock_overlay

        scene = GameScene(game)

        # Verify initial overlay creation
        mock_surface_cls.assert_called_with((800, 600), pygame.SRCALPHA)

        screen = MagicMock()
        screen.get_size.return_value = (800, 600)

        # Mock rendering system to avoid errors inside it
        scene.rendering_system = MagicMock()
        scene.ui_system = MagicMock()
        scene.game_state.map.draw = MagicMock()

        # --- TEST NIGHT ---
        scene.game_state.time_elapsed = 150 # Night (max opacity)

        scene.draw(screen)

        # Verify overlay is NOT recreated if size matches
        assert mock_surface_cls.call_count == 1 # Only from init

        # Verify fill. 150s = pi = cos(-1) = (1 - (-1))/2 = 1.0 * 180 = 180
        args, _ = mock_overlay.fill.call_args
        color = args[0]
        assert color[3] == 180 # Opacity

        # Verify blit
        screen.blit.assert_called_with(mock_overlay, (0, 0))

        # --- TEST DAY ---
        scene.game_state.time_elapsed = 0 # Day (0 opacity)
        screen.reset_mock()
        mock_overlay.reset_mock()

        scene.draw(screen)

        # Should NOT blit overlay if opacity is 0
        screen.blit.assert_not_called()
