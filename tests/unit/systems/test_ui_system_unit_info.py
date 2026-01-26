# pylint: disable=redefined-outer-name
from unittest.mock import MagicMock

import pygame
import pytest

from command_line_conflict.camera import Camera
from command_line_conflict.components.health import Health
from command_line_conflict.components.renderable import Renderable
from command_line_conflict.components.selectable import Selectable
from command_line_conflict.components.unit_identity import UnitIdentity
from command_line_conflict.game_state import GameState
from command_line_conflict.maps.base import Map
from command_line_conflict.systems.ui_system import UISystem


@pytest.fixture
def game_state():
    """Fixture for creating a mock game state."""
    game_map = MagicMock(spec=Map)
    game_state = GameState(game_map)
    return game_state


@pytest.fixture
def ui_system():
    """Fixture for creating a UISystem with a mock screen and camera."""
    pygame.init()
    screen = MagicMock()
    font = MagicMock()
    camera = Camera()
    return UISystem(screen, font, camera)


def test_draw_unit_name_with_identity(ui_system, game_state):
    """Test that the full unit name is displayed when UnitIdentity is present."""
    selectable = Selectable()
    selectable.is_selected = True

    # Create a Rover unit
    game_state.entities = {
        1: {
            UnitIdentity: UnitIdentity(name="rover"),
            Renderable: Renderable(icon="R"),
            Health: Health(hp=100, max_hp=100),
            Selectable: selectable,
        }
    }

    # Mock the font.render method to capture what is being rendered
    ui_system.font.render = MagicMock()

    # We also need to mock small/medium/large fonts because _get_text_surface uses them
    # But _draw_single_unit_info uses the default font (size "normal")

    ui_system.draw(game_state, paused=False)

    # Check if "Unit: Rover" was rendered
    # We look for a call where the first argument is "Unit: Rover"
    calls = ui_system.font.render.call_args_list
    rendered_texts = [call[0][0] for call in calls]

    # Since we haven't implemented the change yet, this should fail (it will render "Unit: R")
    # But for TDD, we assert what we WANT.
    assert "Unit: Rover" in rendered_texts
    assert "Unit: R" not in rendered_texts


def test_draw_unit_name_fallback_to_icon(ui_system, game_state):
    """Test that the icon is displayed when UnitIdentity is missing."""
    selectable = Selectable()
    selectable.is_selected = True

    # Create a Wildlife unit (no identity)
    game_state.entities = {
        1: {
            Renderable: Renderable(icon="w"),
            Health: Health(hp=40, max_hp=40),
            Selectable: selectable,
        }
    }

    ui_system.font.render = MagicMock()
    ui_system.draw(game_state, paused=False)

    calls = ui_system.font.render.call_args_list
    rendered_texts = [call[0][0] for call in calls]

    assert "Unit: w" in rendered_texts
