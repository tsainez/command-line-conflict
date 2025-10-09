from unittest.mock import Mock, call, patch

import pygame

from command_line_conflict import config
from command_line_conflict.camera import Camera
from command_line_conflict.components.dead import Dead
from command_line_conflict.components.movable import Movable
from command_line_conflict.components.position import Position
from command_line_conflict.components.renderable import Renderable
from command_line_conflict.game_state import GameState
from command_line_conflict.systems.rendering_system import RenderingSystem


def test_draw_orders_are_affected_by_camera():
    # Arrange
    mock_screen = Mock()
    mock_font = Mock()
    mock_surface = Mock()
    mock_font.render.return_value = mock_surface

    camera = Camera(x=10, y=5, zoom=2.0)
    rendering_system = RenderingSystem(
        screen=mock_screen, font=mock_font, camera=camera
    )

    mock_map = Mock()
    game_state = GameState(game_map=mock_map)
    entity_id = game_state.create_entity()

    game_state.add_component(entity_id, Position(x=20, y=10))
    movable = Movable(speed=1.0)
    movable.path = [(21, 11), (22, 12)]
    game_state.add_component(entity_id, movable)
    game_state.add_component(entity_id, Renderable(icon="R"))

    components = game_state.entities[entity_id]

    # Act
    rendering_system.draw_orders(components)

    # Assert
    expected_x1 = (21 - camera.x) * config.GRID_SIZE * camera.zoom
    expected_y1 = (11 - camera.y) * config.GRID_SIZE * camera.zoom

    expected_x2 = (22 - camera.x) * config.GRID_SIZE * camera.zoom
    expected_y2 = (12 - camera.y) * config.GRID_SIZE * camera.zoom

    # The character for the arrow from (20, 10) to (21, 11) is '↘'
    assert call("↘", True, (0, 255, 0)) in mock_font.render.call_args_list
    assert call("◎", True, (255, 0, 0)) in mock_font.render.call_args_list

    expected_calls = [
        call(mock_surface, (expected_x1, expected_y1)),
        call(mock_surface, (expected_x2, expected_y2)),
    ]
    mock_screen.blit.assert_has_calls(expected_calls, any_order=True)


@patch("pygame.transform.scale")
def test_draw_entities_are_affected_by_camera(mock_scale):
    # Arrange
    mock_screen = Mock()
    mock_font = Mock()
    mock_surface = Mock()
    # This mock surface will be scaled, so we need a mock for the scaled surface too
    mock_scaled_surface = Mock()
    mock_surface.convert_alpha.return_value = mock_surface
    mock_scale.return_value = mock_scaled_surface
    mock_font.render.return_value = mock_surface

    camera = Camera(x=15, y=25, zoom=1.5)
    rendering_system = RenderingSystem(
        screen=mock_screen, font=mock_font, camera=camera
    )

    mock_map = Mock()
    game_state = GameState(game_map=mock_map)
    entity_id = game_state.create_entity()

    game_state.add_component(entity_id, Position(x=30, y=40))
    game_state.add_component(entity_id, Renderable(icon="E"))

    # Act
    rendering_system.draw(game_state, paused=False)

    # Assert
    expected_x = (30 - camera.x) * config.GRID_SIZE * camera.zoom
    expected_y = (40 - camera.y) * config.GRID_SIZE * camera.zoom

    # Check that font.render was called for the entity's icon
    mock_font.render.assert_any_call("E", True, (255, 255, 255))

    # Check that the surface was scaled
    grid_size = int(config.GRID_SIZE * camera.zoom)
    mock_scale.assert_any_call(mock_surface, (grid_size, grid_size))

    # Check that screen.blit was called with the transformed coordinates
    mock_screen.blit.assert_any_call(mock_scaled_surface, (expected_x, expected_y))


@patch("pygame.transform.scale")
def test_dead_unit_renders_as_skull(mock_scale):
    # Arrange
    mock_screen = Mock()
    mock_font = Mock()
    mock_surface = Mock()
    mock_scaled_surface = Mock()
    mock_surface.convert_alpha.return_value = mock_surface
    mock_scale.return_value = mock_scaled_surface
    mock_font.render.return_value = mock_surface

    camera = Camera(x=0, y=0, zoom=1.0)
    rendering_system = RenderingSystem(
        screen=mock_screen, font=mock_font, camera=camera
    )

    mock_map = Mock()
    game_state = GameState(game_map=mock_map)
    entity_id = game_state.create_entity()

    game_state.add_component(entity_id, Position(x=1, y=1))
    game_state.add_component(entity_id, Renderable(icon="E"))
    game_state.add_component(entity_id, Dead())

    # Act
    rendering_system.draw(game_state, paused=False)

    # Assert
    mock_font.render.assert_any_call("✖", True, (128, 128, 128))


@patch("pygame.transform.scale")
def test_zoom_does_not_misalign_units_with_fractional_positions(mock_scale):
    # Arrange
    mock_screen = Mock()
    mock_font = Mock()
    mock_surface = Mock()
    mock_scaled_surface = Mock()
    mock_surface.convert_alpha.return_value = mock_surface
    mock_scale.return_value = mock_scaled_surface
    mock_font.render.return_value = mock_surface

    camera = Camera(x=0, y=0, zoom=2.0)
    rendering_system = RenderingSystem(
        screen=mock_screen, font=mock_font, camera=camera
    )

    mock_map = Mock()
    game_state = GameState(game_map=mock_map)
    entity_id = game_state.create_entity()

    # Position with a fractional part to test the bug
    unit_pos = Position(x=10.5, y=20.25)
    game_state.add_component(entity_id, unit_pos)
    game_state.add_component(entity_id, Renderable(icon="T"))

    # Act
    rendering_system.draw(game_state, paused=False)

    # Assert
    # The correct calculation should not cast the position to int prematurely.
    # The error comes from (int(10.5) - 0) * 20 * 2.0 = 400, when it should be 420.
    expected_x = (unit_pos.x - camera.x) * config.GRID_SIZE * camera.zoom
    expected_y = (unit_pos.y - camera.y) * config.GRID_SIZE * camera.zoom

    # Check that screen.blit was called with the correctly calculated coordinates
    mock_screen.blit.assert_any_call(mock_scaled_surface, (expected_x, expected_y))
