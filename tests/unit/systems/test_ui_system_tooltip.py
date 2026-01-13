from unittest.mock import MagicMock, patch

import pytest

from command_line_conflict.camera import Camera
from command_line_conflict.components.health import Health
from command_line_conflict.components.player import Player
from command_line_conflict.components.unit_identity import UnitIdentity
from command_line_conflict.game_state import GameState
from command_line_conflict.systems.ui_system import UISystem


@pytest.fixture
def mock_ui_system():
    screen = MagicMock()
    font = MagicMock()
    # Mock font.render to return a surface with size
    mock_surface = MagicMock()
    mock_surface.get_width.return_value = 50
    mock_surface.get_height.return_value = 20
    font.render.return_value = mock_surface

    # Mock small_font
    small_font = MagicMock()
    small_font.render.return_value = mock_surface

    with patch("pygame.font.Font", return_value=small_font):
        ui = UISystem(screen, font, Camera())
        ui.small_font = small_font
        return ui


def test_draw_tooltip_renders_correct_text(mock_ui_system):
    game_state = MagicMock(spec=GameState)
    game_state.entities = {
        1: {UnitIdentity: UnitIdentity("rover"), Health: Health(hp=80, max_hp=100), Player: Player(player_id=1)}
    }
    # .get() is called on the dict

    # We need to make sure _get_text_surface returns a mock surface
    mock_surface = MagicMock()
    mock_surface.get_width.return_value = 50
    mock_surface.get_height.return_value = 20

    # Since _get_text_surface is cached, we can't easily mock it on the instance if it's already bound?
    # But we can inspect the font.render calls instead.

    mock_ui_system.draw(game_state, False, 1, hovered_entity_id=1, mouse_pos=(100, 100))

    # Check if small_font.render was called
    # The text is "Rover (80/100)"
    # Color for player 1 is (100, 255, 100)

    # Note: _get_text_surface calls font.render(text, True, color)
    mock_ui_system.small_font.render.assert_any_call("Rover (80/100)", True, (100, 255, 100))


def test_draw_tooltip_renders_no_hp_if_missing(mock_ui_system):
    game_state = MagicMock(spec=GameState)
    game_state.entities = {1: {UnitIdentity: UnitIdentity("mineral"), Player: Player(player_id=0)}}  # Neutral

    mock_ui_system.draw(game_state, False, 1, hovered_entity_id=1, mouse_pos=(100, 100))

    # Color for neutral is (200, 200, 200)
    mock_ui_system.small_font.render.assert_any_call("Mineral", True, (200, 200, 200))
