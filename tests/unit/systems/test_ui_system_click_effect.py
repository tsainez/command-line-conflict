from unittest.mock import MagicMock, patch

import pygame
import pytest

from command_line_conflict.camera import Camera
from command_line_conflict.game_state import GameState
from command_line_conflict.maps.base import Map
from command_line_conflict.systems.ui_system import UISystem


@pytest.fixture
def ui_system():
    pygame.init()
    screen = MagicMock()
    font = MagicMock()
    camera = Camera()
    return UISystem(screen, font, camera)


@patch("pygame.draw.circle")
@patch("pygame.time.get_ticks")
def test_click_effect(mock_get_ticks, mock_draw_circle, ui_system):
    # Setup
    mock_get_ticks.return_value = 1000
    game_state = GameState(MagicMock(spec=Map))

    # Add effect
    ui_system.add_click_effect(10, 10, (0, 255, 0))

    # Assert added
    assert len(ui_system.click_effects) == 1
    assert ui_system.click_effects[0]["x"] == 10

    # Draw (simulate time passing)
    mock_get_ticks.return_value = 1100  # 100ms passed
    ui_system.draw(game_state, paused=False)

    # Assert drawn
    mock_draw_circle.assert_called()

    # Check if it cleans up
    mock_get_ticks.return_value = 1600  # 600ms passed (duration is 500)
    ui_system.draw(game_state, paused=False)

    # Should be empty now
    assert len(ui_system.click_effects) == 0
