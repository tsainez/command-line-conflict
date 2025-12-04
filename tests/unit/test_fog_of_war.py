
import pytest
from command_line_conflict.fog_of_war import FogOfWar

class MockUnit:
    def __init__(self, x, y, vision_range):
        self.x = x
        self.y = y
        self.vision_range = vision_range

def test_fog_of_war_initialization():
    fow = FogOfWar(10, 10)
    assert fow.width == 10
    assert fow.height == 10
    assert len(fow.grid) == 10
    assert len(fow.grid[0]) == 10
    assert fow.grid[0][0] == FogOfWar.HIDDEN

def test_fog_of_war_update_visibility():
    fow = FogOfWar(10, 10)
    unit = MockUnit(x=5, y=5, vision_range=2)

    fow.update([unit])

    # Center should be visible
    assert fow.grid[5][5] == FogOfWar.VISIBLE

    # Within range should be visible (e.g., 5,7 is dist 2)
    assert fow.grid[7][5] == FogOfWar.VISIBLE

    # Outside range should be hidden (e.g., 0,0)
    assert fow.grid[0][0] == FogOfWar.HIDDEN

def test_fog_of_war_downgrade_to_explored():
    fow = FogOfWar(10, 10)
    unit = MockUnit(x=5, y=5, vision_range=2)

    # First update: Make area visible
    fow.update([unit])
    assert fow.grid[5][5] == FogOfWar.VISIBLE

    # Move unit away
    unit.x = 0
    unit.y = 0
    fow.update([unit])

    # Old area should be EXPLORED
    assert fow.grid[5][5] == FogOfWar.EXPLORED

    # New area should be VISIBLE
    assert fow.grid[0][0] == FogOfWar.VISIBLE
