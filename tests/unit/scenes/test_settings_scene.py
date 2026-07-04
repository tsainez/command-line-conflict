from unittest.mock import MagicMock

import pygame
import pytest

from command_line_conflict import config
from command_line_conflict.scenes.settings import SettingsScene


@pytest.fixture
def mock_game():
    game = MagicMock()
    game.screen = MagicMock()
    game.screen.get_width.return_value = 800
    game.screen.get_height.return_value = 600
    game.font = MagicMock()
    game.music_manager = MagicMock()
    return game


@pytest.fixture
def settings_scene(mock_game):
    return SettingsScene(mock_game)


def test_initialization(settings_scene):
    assert settings_scene.selected_option == 0
    assert "Screen Size" in settings_scene.settings_options


def test_handle_key_down(settings_scene):
    event = MagicMock()
    event.type = pygame.KEYDOWN
    event.key = pygame.K_DOWN

    settings_scene.handle_event(event)
    assert settings_scene.selected_option == 1


def test_handle_key_up(settings_scene):
    settings_scene.selected_option = 1
    event = MagicMock()
    event.type = pygame.KEYDOWN
    event.key = pygame.K_UP

    settings_scene.handle_event(event)
    assert settings_scene.selected_option == 0


def test_change_volume(settings_scene):
    config.MASTER_VOLUME = 0.5  # Set to a known value
    settings_scene.selected_option = 2  # Master Volume
    original_volume = config.MASTER_VOLUME

    event = MagicMock()
    event.type = pygame.KEYDOWN
    event.key = pygame.K_RIGHT

    settings_scene.handle_event(event)
    assert config.MASTER_VOLUME > original_volume


def test_toggle_debug(settings_scene):
    settings_scene.selected_option = 1  # Debug Mode
    original_debug = config.DEBUG

    event = MagicMock()
    event.type = pygame.KEYDOWN
    event.key = pygame.K_RETURN

    settings_scene.handle_event(event)
    assert config.DEBUG != original_debug
    # Revert
    config.DEBUG = original_debug


def test_mouse_hover(settings_scene):
    # Setup option rects
    rect0 = MagicMock()
    rect0.collidepoint.return_value = False
    rect1 = MagicMock()
    rect1.collidepoint.return_value = True  # Hovering over 2nd option
    settings_scene.option_rects = [(rect0, 0), (rect1, 1)]

    event = MagicMock()
    event.type = pygame.MOUSEMOTION
    event.pos = (100, 100)

    settings_scene.handle_event(event)
    assert settings_scene.selected_option == 1


def test_mouse_click_volume_right(settings_scene):
    config.MASTER_VOLUME = 0.5
    original_volume = config.MASTER_VOLUME

    # Master Volume is index 2
    rect = MagicMock()
    rect.collidepoint.return_value = True
    rect.centerx = 100
    settings_scene.option_rects = [(rect, 2)]

    event = MagicMock()
    event.type = pygame.MOUSEBUTTONUP
    event.button = 1
    event.pos = (150, 100)  # Right side

    settings_scene.handle_event(event)
    assert config.MASTER_VOLUME > original_volume


def test_mouse_click_volume_left(settings_scene):
    config.MASTER_VOLUME = 0.5
    original_volume = config.MASTER_VOLUME

    # Master Volume is index 2
    rect = MagicMock()
    rect.collidepoint.return_value = True
    rect.centerx = 100
    settings_scene.option_rects = [(rect, 2)]

    event = MagicMock()
    event.type = pygame.MOUSEBUTTONUP
    event.button = 1
    event.pos = (50, 100)  # Left side

    settings_scene.handle_event(event)
    assert config.MASTER_VOLUME < original_volume


def test_mouse_click_trigger(settings_scene):
    back_index = settings_scene.settings_options.index("Back")
    rect = MagicMock()
    rect.collidepoint.return_value = True
    settings_scene.option_rects = [(rect, back_index)]

    event = MagicMock()
    event.type = pygame.MOUSEBUTTONUP
    event.button = 1
    event.pos = (100, 100)

    settings_scene.handle_event(event)
    settings_scene.game.scene_manager.switch_to.assert_called_with("menu")


def test_scroll_wheel_volume_is_static(settings_scene):
    """Wheel up always increases and wheel down always decreases volume,
    regardless of which side of the bar the cursor sits on."""
    config.MASTER_VOLUME = 0.5

    rect = MagicMock()
    rect.collidepoint.return_value = True
    rect.centerx = 100
    settings_scene.option_rects = [(rect, 2)]  # Master Volume

    # Wheel up with the cursor on the LEFT half (the old position-based
    # logic would have decreased here).
    event = MagicMock()
    event.type = pygame.MOUSEBUTTONUP
    event.button = 4
    event.pos = (50, 100)
    settings_scene.handle_event(event)
    assert config.MASTER_VOLUME > 0.5

    # Wheel down with the cursor on the RIGHT half.
    config.MASTER_VOLUME = 0.5
    event = MagicMock()
    event.type = pygame.MOUSEBUTTONUP
    event.button = 5
    event.pos = (150, 100)
    settings_scene.handle_event(event)
    assert config.MASTER_VOLUME < 0.5


def test_scroll_wheel_does_not_trigger_options(settings_scene):
    """A wheel tick over a non-volume row (e.g. Back) must do nothing."""
    back_index = settings_scene.settings_options.index("Back")
    rect = MagicMock()
    rect.collidepoint.return_value = True
    settings_scene.option_rects = [(rect, back_index)]

    event = MagicMock()
    event.type = pygame.MOUSEBUTTONUP
    event.button = 4
    event.pos = (100, 100)

    settings_scene.handle_event(event)
    settings_scene.game.scene_manager.switch_to.assert_not_called()


def test_settings_layout_fits_smallest_screen(settings_scene):
    """All option rows plus the help line must fit 800x600 without overlap."""
    last_row_center = settings_scene.options_start_y + (len(settings_scene.settings_options) - 1) * (
        settings_scene.option_spacing
    )
    # Option font is 50px tall; help text is centered at height - 50.
    assert last_row_center + 25 < 600 - 50 - 10


def test_escape_key_navigates_back(settings_scene):
    event = MagicMock()
    event.type = pygame.KEYDOWN
    event.key = pygame.K_ESCAPE

    settings_scene.handle_event(event)
    settings_scene.game.scene_manager.switch_to.assert_called_with("menu")
