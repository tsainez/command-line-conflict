from unittest.mock import MagicMock

import pygame
import pytest

from command_line_conflict.engine import Game


@pytest.fixture
def mock_dependencies(mocker):
    mocker.patch("command_line_conflict.engine.MusicManager")
    mocker.patch("command_line_conflict.engine.SteamIntegration")
    # Patch pygame.time.Clock so we can control tick and avoid read-only errors
    mocker.patch("pygame.time.Clock")
    # Patch display.flip and quit to avoid real pygame calls failing
    mocker.patch("pygame.display.flip")
    mocker.patch("pygame.quit")


def test_game_initialization(mock_dependencies):
    game = Game()
    assert game.running is True
    assert game.scene_manager is not None
    assert game.clock is not None


def test_game_run_loop(mock_dependencies, mocker):
    game = Game()

    # Mock scene manager
    game.scene_manager = MagicMock()

    # Mock clock.tick
    game.clock.tick.return_value = 16

    # Create a quit event
    mock_event = MagicMock()
    mock_event.type = pygame.QUIT

    # Mock pygame.event.get to return the quit event
    mocker.patch("pygame.event.get", side_effect=[[mock_event]])

    game.run()

    assert game.running is False
    # Verify scene manager methods were called
    game.scene_manager.handle_event.assert_called_with(mock_event)
    game.scene_manager.update.assert_called_once()
    game.scene_manager.draw.assert_called_once()
