from types import SimpleNamespace

import pytest

from command_line_conflict.fog_of_war import FogOfWar


class TestFogOptimization:
    def test_update_optimizes_stationary_units(self, mocker):
        # Mock PixelArray to avoid issues with mocked Surface
        m_pixelarray = mocker.patch("command_line_conflict.fog_of_war.pygame.PixelArray")

        width, height = 20, 20
        fog = FogOfWar(width, height)

        unit = SimpleNamespace(x=10, y=10, vision_range=5)
        units = [unit]

        # First update - should process
        fog.update(units)

        # Verify PixelArray was used (implying full update)
        # Note: FogOfWar only creates PixelArray if visible_cells changed.
        # Initial visible_cells is empty, so it should update.
        assert m_pixelarray.call_count == 1
        m_pixelarray.reset_mock()

        # Second update - same position
        # Create new list with new objects but same values to simulate game loop
        units_same = [SimpleNamespace(x=10, y=10, vision_range=5)]
        fog.update(units_same)

        # Verify PixelArray was NOT used (early return)
        assert m_pixelarray.call_count == 0

        # Third update - moved unit
        units_moved = [SimpleNamespace(x=11, y=10, vision_range=5)]
        fog.update(units_moved)

        # Verify PixelArray WAS used again
        assert m_pixelarray.call_count == 1

    def test_update_handles_vision_range_change(self, mocker):
        m_pixelarray = mocker.patch("command_line_conflict.fog_of_war.pygame.PixelArray")
        width, height = 20, 20
        fog = FogOfWar(width, height)

        unit = SimpleNamespace(x=10, y=10, vision_range=5)
        fog.update([unit])
        m_pixelarray.reset_mock()

        # Change vision range
        unit.vision_range = 6
        fog.update([unit])

        assert m_pixelarray.call_count == 1
