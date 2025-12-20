from unittest.mock import Mock, patch

from command_line_conflict.camera import Camera
from command_line_conflict.components.health import Health
from command_line_conflict.components.position import Position
from command_line_conflict.components.renderable import Renderable
from command_line_conflict.game_state import GameState
from command_line_conflict.systems.rendering_system import RenderingSystem


@patch("pygame.draw.rect")
@patch("pygame.transform.scale")
def test_draw_health_bar(mock_scale, mock_draw_rect):
    # Arrange
    mock_screen = Mock()
    mock_screen.get_width.return_value = 800
    mock_screen.get_height.return_value = 600
    mock_font = Mock()
    mock_surface = Mock()
    mock_scaled_surface = Mock()
    mock_scale.return_value = mock_scaled_surface
    mock_font.render.return_value = mock_surface

    camera = Camera(x=0, y=0, zoom=1.0)
    rendering_system = RenderingSystem(screen=mock_screen, font=mock_font, camera=camera)

    mock_map = Mock()
    game_state = GameState(game_map=mock_map)
    entity_id = game_state.create_entity()

    game_state.add_component(entity_id, Position(x=10, y=10))
    game_state.add_component(entity_id, Renderable(icon="U"))
    game_state.add_component(entity_id, Health(hp=50, max_hp=100))

    # Act
    rendering_system.draw(game_state, paused=False)

    # Assert
    # We expect pygame.draw.rect to be called for the health bar
    # One for background (maybe), one for health
    # For now let's just assert it was called at all
    assert mock_draw_rect.called
