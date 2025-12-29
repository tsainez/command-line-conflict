from types import SimpleNamespace
from unittest.mock import Mock

from command_line_conflict.fog_of_war import FogOfWar


class TestFogOfWar:
    def test_initialization(self, mocker):
        # fog.fog_texture is a Mock because pygame.Surface is mocked in conftest
        width, height = 10, 10
        fog = FogOfWar(width, height)

        assert fog.width == width
        assert fog.height == height
        assert len(fog.grid) == height
        assert len(fog.grid[0]) == width

        # Verify fog_texture creation
        assert fog.fog_texture is not None

        # Verify it was filled with hidden color
        fog.fog_texture.fill.assert_called_with(FogOfWar.COLOR_HIDDEN)

    def test_update_visibility(self, mocker):
        # Mock PixelArray
        mock_pixel_array_cls = mocker.patch("pygame.PixelArray")
        mock_px = mock_pixel_array_cls.return_value
        # Allow px[x,y] assignment
        mock_px.__setitem__ = Mock()

        width, height = 10, 10
        fog = FogOfWar(width, height)

        # Create a mock unit
        unit = SimpleNamespace(x=5, y=5, vision_range=2)

        # Initial state: all hidden
        assert fog.grid[5][5] == FogOfWar.HIDDEN

        # Update with the unit
        fog.update([unit])

        # Check that the unit's position is visible in GRID
        assert fog.grid[5][5] == FogOfWar.VISIBLE
        # Check a tile within range
        assert fog.grid[6][5] == FogOfWar.VISIBLE
        # Check a tile out of range
        assert fog.grid[0][0] == FogOfWar.HIDDEN

    def test_update_downgrade_to_explored(self, mocker):
        mocker.patch("pygame.PixelArray")

        width, height = 10, 10
        fog = FogOfWar(width, height)

        unit1 = SimpleNamespace(x=5, y=5, vision_range=1)

        # First update: make some tiles visible
        fog.update([unit1])
        assert fog.grid[5][5] == FogOfWar.VISIBLE

        # Move unit away
        unit2 = SimpleNamespace(x=0, y=0, vision_range=1)

        # Update with new position
        fog.update([unit2])

        # Old position should be EXPLORED
        assert fog.grid[5][5] == FogOfWar.EXPLORED
        # New position should be VISIBLE
        assert fog.grid[0][0] == FogOfWar.VISIBLE

    def test_draw_uses_scale_and_blit(self, mocker):
        # Patch transform.scale
        mock_scale = mocker.patch("pygame.transform.scale")
        mock_smoothscale = mocker.patch("pygame.transform.smoothscale")
        mock_scaled_surf = Mock()
        mock_scale.return_value = mock_scaled_surf
        mock_smoothscale.return_value = mock_scaled_surf

        width, height = 10, 10
        fog = FogOfWar(width, height)

        screen = Mock()
        screen.get_size.return_value = (800, 600)

        fog.draw(screen)

        # Should use smoothscale
        mock_smoothscale.assert_called_with(fog.fog_texture, (200, 200))

        screen.blit.assert_called_with(mock_scaled_surf, (0, 0))

    def test_draw_fallback_on_error(self, mocker):
        import pygame
        mock_scale = mocker.patch("pygame.transform.scale")
        mock_smoothscale = mocker.patch("pygame.transform.smoothscale")

        # Smoothscale fails
        mock_smoothscale.side_effect = pygame.error("Smoothscale failed")

        mock_scaled_surf = Mock()
        mock_scale.return_value = mock_scaled_surf

        width, height = 10, 10
        fog = FogOfWar(width, height)
        screen = Mock()
        screen.get_size.return_value = (800, 600)

        fog.draw(screen)

        # Verify smoothscale was tried
        mock_smoothscale.assert_called()
        # Verify fallback to scale
        mock_scale.assert_called()

        screen.blit.assert_called_with(mock_scaled_surf, (0, 0))

    def test_draw_with_camera(self, mocker):
        mock_smoothscale = mocker.patch("pygame.transform.smoothscale")
        mock_scaled_surf = Mock()
        mock_smoothscale.return_value = mock_scaled_surf

        width, height = 100, 100
        fog = FogOfWar(width, height)

        # Make subsurface work on the mock texture
        mock_subsurface = Mock()
        fog.fog_texture.subsurface.return_value = mock_subsurface

        screen = Mock()
        screen.get_size.return_value = (800, 600)

        camera = Mock()
        camera.x = 10
        camera.y = 10
        camera.zoom = 1.0

        fog.draw(screen, camera)

        # Should call subsurface
        fog.fog_texture.subsurface.assert_called()

        # Should call smoothscale on subsurface
        args, _ = mock_smoothscale.call_args
        assert args[0] == mock_subsurface

        # Should blit
        screen.blit.assert_called_with(mock_scaled_surf, (0, 0))
