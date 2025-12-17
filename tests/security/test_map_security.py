import json
import unittest
from command_line_conflict.maps.base import Map

class TestMapSecurity(unittest.TestCase):
    def test_map_dimension_limit_init(self):
        """Test that creating a map with excessive dimensions raises a ValueError."""
        # We expect a limit (e.g., 256). 1000 should fail.
        with self.assertRaises(ValueError):
            Map(width=1000, height=1000)

    def test_map_dimension_limit_load(self):
        """Test loading a map with huge dimensions via from_dict."""
        data = {
            "width": 10000,
            "height": 10000,
            "walls": []
        }
        with self.assertRaises(ValueError):
            Map.from_dict(data)

    def test_negative_dimensions(self):
        """Test that negative dimensions are rejected."""
        with self.assertRaises(ValueError):
            Map(width=-1, height=10)
        with self.assertRaises(ValueError):
            Map(width=10, height=-1)

    def test_wall_bounds_validation(self):
        """Test that walls outside the map boundaries are filtered out."""
        # We want to ensure that if a map file contains walls outside bounds,
        # they are ignored to prevent logic errors later.
        data = {
            "width": 10,
            "height": 10,
            "walls": [[-1, 5], [10, 5], [5, 5]] # Only [5, 5] is valid
        }
        m = Map.from_dict(data)

        # Check that only valid walls remain
        self.assertIn((5, 5), m.walls)
        self.assertNotIn((-1, 5), m.walls)
        self.assertNotIn((10, 5), m.walls)
        self.assertEqual(len(m.walls), 1)
