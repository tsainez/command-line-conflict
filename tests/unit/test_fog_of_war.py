from types import SimpleNamespace
from unittest.mock import Mock

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

        assert fog.surface is None

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

    def test_draw_initial_fill(self, mocker):
        # Test that we create a surface and fill it with black
        mocker.patch("pygame.Surface")
        import pygame

        width, height = 10, 10
        fog = FogOfWar(width, height)

        screen = Mock()
        screen.get_size.return_value = (800, 600)

        mock_fog_surface = Mock()
        mock_fog_surface.get_size.return_value = (800, 600)
        pygame.Surface.return_value = mock_fog_surface

        fog.draw(screen)

        # Verify surface creation
        pygame.Surface.assert_called_with((800, 600), pygame.SRCALPHA)

        # Verify fill with black (HIDDEN)
        mock_fog_surface.fill.assert_any_call((0, 0, 0, 255))

        # Verify blit to screen
        screen.blit.assert_called_with(mock_fog_surface, (0, 0))

    def test_draw_visible_and_explored(self, mocker):
        mocker.patch("pygame.Surface")
        import pygame

        width, height = 2, 2
        fog = FogOfWar(width, height)

        # Set states
        fog.grid[0][0] = FogOfWar.VISIBLE
        fog.grid[0][1] = FogOfWar.EXPLORED
        # (1,0) and (1,1) are HIDDEN

        screen = Mock()
        screen.get_size.return_value = (100, 100)

        mock_fog_surface = Mock()
        mock_fog_surface.get_size.return_value = (100, 100)
        pygame.Surface.return_value = mock_fog_surface

        fog.draw(screen)

        # Verify fill black
        mock_fog_surface.fill.assert_any_call((0, 0, 0, 255))

        # Verify visible (0,0) -> Transparent
        size = config.GRID_SIZE + 1
        visible_rect = (0, 0, size, size)
        mock_fog_surface.fill.assert_any_call((0, 0, 0, 0), visible_rect)

        # Verify explored (0,1) -> y=0, x=1 -> Semi-transparent
        explored_rect = (config.GRID_SIZE, 0, size, size)
        mock_fog_surface.fill.assert_any_call((0, 0, 0, 180), explored_rect)

        # Verify we only have 2 rect fills (plus the initial full fill)
        # 1 initial fill: (0,0,0,255) without rect
        # 2 rect fills: with rect
        calls = mock_fog_surface.fill.call_args_list
        rect_fills = [c for c in calls if len(c[0]) == 2]  # fill(color, rect)
        assert len(rect_fills) == 2

    def test_draw_resize_surface(self, mocker):
        # If screen size changes, surface should be recreated
        mocker.patch("pygame.Surface")
        import pygame

        fog = FogOfWar(10, 10)

        screen1 = Mock()
        screen1.get_size.return_value = (800, 600)

        mock_surf1 = Mock()
        mock_surf1.get_size.return_value = (800, 600)

        mock_surf2 = Mock()
        mock_surf2.get_size.return_value = (1024, 768)

        pygame.Surface.side_effect = [mock_surf1, mock_surf2]

        fog.draw(screen1)
        assert fog.surface == mock_surf1

        # Resize screen
        screen2 = Mock()
        screen2.get_size.return_value = (1024, 768)

        fog.draw(screen2)
        assert fog.surface == mock_surf2

        assert pygame.Surface.call_count == 2
