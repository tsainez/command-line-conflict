import pytest
import pygame

@pytest.fixture(autouse=True)
def mock_pygame(mocker):
    """Mock pygame to avoid display initialization."""
    mocker.patch("pygame.display.set_mode", return_value=mocker.MagicMock())
    mocker.patch("pygame.display.set_caption", return_value=mocker.MagicMock())
    mocker.patch("pygame.font.Font", return_value=mocker.MagicMock())
    mocker.patch("pygame.font.SysFont", return_value=mocker.MagicMock())
    mocker.patch("pygame.font.match_font", return_value=mocker.MagicMock())
    mocker.patch("pygame.Surface", new=mocker.MagicMock())
    mocker.patch("pygame.draw.line", return_value=mocker.MagicMock())
    mocker.patch("pygame.draw.rect", return_value=mocker.MagicMock())
    mocker.patch("pygame.event.get", return_value=[])
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture
def game_state():
    """
    Returns a GameState object with a SimpleMap.
    """
    from command_line_conflict.game_state import GameState
    from command_line_conflict.maps.simple_map import SimpleMap
    game_map = SimpleMap()
    return GameState(game_map)
