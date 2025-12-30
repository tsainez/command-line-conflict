# pylint: disable=redefined-outer-name
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
    event.pos = (50, 100)  # Left side

    settings_scene.handle_event(event)
    assert config.MASTER_VOLUME < original_volume


def test_mouse_click_trigger(settings_scene):
    # Back is index 5
    rect = MagicMock()
    rect.collidepoint.return_value = True
    settings_scene.option_rects = [(rect, 5)]

    event = MagicMock()
    event.type = pygame.MOUSEBUTTONUP
    event.pos = (100, 100)

    settings_scene.handle_event(event)
    settings_scene.game.scene_manager.switch_to.assert_called_with("menu")
