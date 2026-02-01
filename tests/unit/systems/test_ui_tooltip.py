from unittest.mock import MagicMock, patch

import pygame
import pytest

from command_line_conflict.camera import Camera
from command_line_conflict.components.attack import Attack
from command_line_conflict.components.health import Health
from command_line_conflict.components.player import Player
from command_line_conflict.components.unit_identity import UnitIdentity
from command_line_conflict.game_state import GameState
from command_line_conflict.maps.base import Map
from command_line_conflict.systems.ui_system import UISystem


@pytest.fixture
def game_state():
    """Fixture for creating a mock game state."""
    game_map = MagicMock(spec=Map)
    game_state = GameState(game_map)
    game_state.entities = {
        1: {
            UnitIdentity: UnitIdentity(name="Test Unit"),
            Health: Health(hp=100, max_hp=100),
            Attack: Attack(attack_damage=15, attack_range=8, attack_speed=1.0),
            Player: Player(player_id=1),
        }
    }
    return game_state


@pytest.fixture
def ui_system():
    """Fixture for creating a UISystem with a mock screen and camera."""
    # We don't necessarily need pygame.init() if we are mocking everything,
    # but it helps if we touch real pygame objects.
    if not pygame.get_init():
        pygame.init()

    screen = MagicMock()
    font = MagicMock()
    # Mock font.size to return a predictable width
    font.size.return_value = (50, 16)

    with patch("pygame.font.Font") as mock_font_class:
        mock_font_instance = MagicMock()
        # Simplify the return value mock to avoid spec issues
        mock_font_instance.render.return_value = MagicMock()
        mock_font_instance.size.return_value = (50, 16)
        mock_font_class.return_value = mock_font_instance

        camera = Camera()
        system = UISystem(screen, font, camera)
        # Ensure system.small_font is our mock
        system.small_font = mock_font_instance
        return system


def test_draw_tooltip_shows_attack_stats(ui_system, game_state):
    """Test that the tooltip includes attack damage and range."""
    # Call draw_tooltip
    ui_system.draw_tooltip(game_state, 1, (100, 100))

    # Check calls to render
    # We expect calls for: Name, HP, Attack Stats, Player
    rendered_texts = []
    for call in ui_system.small_font.render.call_args_list:
        args, _ = call
        rendered_texts.append(args[0])

    print(f"Rendered texts: {rendered_texts}")

    # Check for Name
    assert "Test Unit" in rendered_texts or "Test unit" in rendered_texts

    # Check for HP
    assert any("HP: 100/100" in t for t in rendered_texts)

    # Check for Attack Stats (This is what we are adding)
    # Expected format: "Dmg: 15 | Rng: 8" or similar
    assert any("Dmg: 15" in t and "Rng: 8" in t for t in rendered_texts)
