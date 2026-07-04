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
    game_state.component_index = {Selectable: {1}}

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
    game_state.component_index = {Selectable: {1}}

    ui_system.font.render = MagicMock()
    ui_system.draw(game_state, paused=False)

    calls = ui_system.font.render.call_args_list
    rendered_texts = [call[0][0] for call in calls]

    assert "Unit: w" in rendered_texts


def test_draw_rover_factory_production_info(ui_system, game_state):
    """Test that factory production and research options are drawn when Rover Factory is selected."""
    from command_line_conflict.campaign_manager import CampaignManager
    from command_line_conflict.components.player import Player

    selectable = Selectable()
    selectable.is_selected = True

    # Create campaign manager on game_state
    cm = CampaignManager()
    if "arachnotron" in cm.unlocked_units:
        cm.unlocked_units.remove("arachnotron")
    game_state.campaign_manager = cm
    game_state.resources[1] = 150

    # Create a Rover Factory entity
    game_state.entities = {
        1: {
            UnitIdentity: UnitIdentity(name="rover_factory"),
            Renderable: Renderable(icon="F"),
            Health: Health(hp=200, max_hp=200),
            Player: Player(player_id=1, is_human=True),
            Selectable: selectable,
        }
    }
    game_state.component_index = {Selectable: {1}, UnitIdentity: {1}}

    # Mock the fonts
    ui_system.font.render = MagicMock()
    ui_system.small_font.render = MagicMock()

    ui_system.draw(game_state, paused=False, current_player_id=1)

    # Check if hints were rendered
    calls = ui_system.small_font.render.call_args_list
    rendered_texts = [call[0][0] for call in calls]

    assert any("Train Chassis" in text for text in rendered_texts)
    assert any("Research Arachnotron" in text for text in rendered_texts)


def test_draw_arachnotron_factory_production_info(ui_system, game_state):
    """Test that factory production options are drawn when Arachnotron Factory is selected."""
    from command_line_conflict.components.player import Player
    from command_line_conflict.components.position import Position

    selectable = Selectable()
    selectable.is_selected = True

    game_state.resources[1] = 200

    # Create an Arachnotron Factory entity
    factory_id = 1
    game_state.entities = {
        factory_id: {
            UnitIdentity: UnitIdentity(name="arachnotron_factory"),
            Renderable: Renderable(icon="F"),
            Health: Health(hp=300, max_hp=300),
            Player: Player(player_id=1, is_human=True),
            Selectable: selectable,
            Position: Position(x=15.0, y=15.0),
        }
    }
    game_state.component_index = {Selectable: {factory_id}, UnitIdentity: {factory_id}}

    # Also add an adjacent friendly Rover
    rover_id = 2
    game_state.entities[rover_id] = {
        UnitIdentity: UnitIdentity(name="rover"),
        Renderable: Renderable(icon="R"),
        Health: Health(hp=100, max_hp=100),
        Player: Player(player_id=1, is_human=True),
        Position: Position(x=15.0, y=14.0),
    }
    game_state.component_index[UnitIdentity].add(rover_id)
    game_state.update_entity_position(rover_id, 15.0, 14.0)

    # Mock the fonts
    ui_system.font.render = MagicMock()
    ui_system.small_font.render = MagicMock()

    ui_system.draw(game_state, paused=False, current_player_id=1)

    # Check if hints were rendered
    calls = ui_system.small_font.render.call_args_list
    rendered_texts = [call[0][0] for call in calls]

    assert any("Train Rover" in text for text in rendered_texts)
    assert any("Train Arachnotron" in text for text in rendered_texts)
