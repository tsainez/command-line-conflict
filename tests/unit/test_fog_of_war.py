from types import SimpleNamespace
from unittest.mock import Mock, call

import pytest

from command_line_conflict import config
from command_line_conflict.fog_of_war import FogOfWar


class TestFogOfWar:
    def test_initialization(self, mocker):
        mocker.patch("pygame.Surface")
        width, height = 10, 10
        fog = FogOfWar(width, height)

        assert fog.width == width
        assert fog.height == height
        assert len(fog.grid) == height
        assert len(fog.grid[0]) == width
        for row in fog.grid:
            for cell in row:
                assert cell == FogOfWar.HIDDEN

        # Check that pygame.Surface was called with correct dimensions
        # Note: default_api:read_file on fog_of_war.py shows
        # pygame.Surface((width * config.GRID_SIZE, height * config.GRID_SIZE), pygame.SRCALPHA)
        # We need to ensure config.GRID_SIZE is available or mocked if it's not a constant.
        # config.GRID_SIZE is likely a constant.

    def test_update_visibility(self):
        width, height = 10, 10
        fog = FogOfWar(width, height)

        # Create a mock unit
        unit = SimpleNamespace(x=5, y=5, vision_range=2)

        # Initial state: all hidden
        assert fog.grid[5][5] == FogOfWar.HIDDEN

        # Update with the unit
        fog.update([unit])

        # Check that the unit's position is visible
        assert fog.grid[5][5] == FogOfWar.VISIBLE
        # Check a tile within range
        assert fog.grid[6][5] == FogOfWar.VISIBLE
        # Check a tile out of range
        assert fog.grid[0][0] == FogOfWar.HIDDEN

    def test_update_downgrade_to_explored(self):
        width, height = 10, 10
        fog = FogOfWar(width, height)

        unit1 = SimpleNamespace(x=5, y=5, vision_range=1)

        # First update: make some tiles visible
        fog.update([unit1])
        assert fog.grid[5][5] == FogOfWar.VISIBLE

        # Move unit away or remove it
        unit2 = SimpleNamespace(x=0, y=0, vision_range=1)

        # Update with new position
        fog.update([unit2])

        # Old position should be EXPLORED
        assert fog.grid[5][5] == FogOfWar.EXPLORED
        # New position should be VISIBLE
        assert fog.grid[0][0] == FogOfWar.VISIBLE

    def test_draw_hidden(self, mocker):
        # Mock pygame.draw.rect
        mock_draw_rect = mocker.patch("pygame.draw.rect")
        mocker.patch("pygame.Surface")

        width, height = 2, 2
        fog = FogOfWar(width, height)

        screen = Mock()
        fog.draw(screen)

        # Should draw rectangles for hidden tiles (black, alpha 255)
        # Grid is all hidden initially.
        # 2x2 grid = 4 calls.
        assert mock_draw_rect.call_count == 4

        # Inspect arguments of first call
        # args: (surface, color, rect)
        args, _ = mock_draw_rect.call_args_list[0]
        color = args[1]
        assert color == (0, 0, 0, 255)

    def test_draw_explored(self, mocker):
        mock_draw_rect = mocker.patch("pygame.draw.rect")
        mocker.patch("pygame.Surface")

        width, height = 2, 2
        fog = FogOfWar(width, height)

        # Manually set a tile to EXPLORED
        fog.grid[0][0] = FogOfWar.EXPLORED

        screen = Mock()
        fog.draw(screen)

        # One tile is EXPLORED, others are HIDDEN. All drawn.
        assert mock_draw_rect.call_count == 4

        # Check calls for the explored tile
        # We need to find the call corresponding to (0,0)
        # Rect is x, y, size, size.
        # x=0, y=0 -> rect should be (0, 0, GRID_SIZE, GRID_SIZE)

        grid_size = config.GRID_SIZE
        found_explored = False
        for call_args in mock_draw_rect.call_args_list:
            args, _ = call_args
            color = args[1]
            rect = args[2]
            if rect[0] == 0 and rect[1] == 0:
                 if color == (0, 0, 0, 180):
                     found_explored = True

        assert found_explored

    def test_draw_visible(self, mocker):
        mock_draw_rect = mocker.patch("pygame.draw.rect")
        mocker.patch("pygame.Surface")

        width, height = 2, 2
        fog = FogOfWar(width, height)

        # Manually set a tile to VISIBLE
        fog.grid[0][0] = FogOfWar.VISIBLE

        screen = Mock()
        fog.draw(screen)

        # Visible tiles are NOT drawn (transparent)
        # So we expect 3 calls (for the 3 hidden tiles) instead of 4
        assert mock_draw_rect.call_count == 3
