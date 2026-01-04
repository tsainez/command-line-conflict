import unittest

from command_line_conflict.maps.wall_map import WallMap


class TestWallMap(unittest.TestCase):
    def test_initialization(self):
        """Test that the WallMap initializes with correct dimensions and walls."""
        wall_map = WallMap()

        self.assertEqual(wall_map.width, 20)
        self.assertEqual(wall_map.height, 15)

        # Check walls
        for x in range(3, 17):
            if x != 10:
                self.assertTrue(wall_map.is_blocked(x, 7), f"Expected wall at ({x}, 7)")
            else:
                self.assertFalse(wall_map.is_blocked(x, 7), f"Expected gap at ({x}, 7)")

    def test_is_walkable(self):
        """Test that walkable areas are correct."""
        wall_map = WallMap()

        # Open area
        self.assertTrue(wall_map.is_walkable(0, 0))
        # Wall
        self.assertFalse(wall_map.is_walkable(3, 7))
        # Gap
        self.assertTrue(wall_map.is_walkable(10, 7))


if __name__ == "__main__":
    unittest.main()
