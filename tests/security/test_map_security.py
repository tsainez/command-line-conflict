import unittest
from command_line_conflict.maps.base import Map

class TestMapSecurity(unittest.TestCase):
    def test_map_dimensions_limit(self):
        """Verify that maps exceeding MAX_MAP_DIMENSION cannot be created."""
        limit = Map.MAX_MAP_DIMENSION

        # Boundary check: limit is fine
        m = Map(limit, limit)
        self.assertEqual(m.width, limit)

        # Limit + 1 raises ValueError
        with self.assertRaises(ValueError):
            Map(limit + 1, limit)

        with self.assertRaises(ValueError):
            Map(limit, limit + 1)

    def test_from_dict_limits(self):
        """Verify from_dict respects dimension limits."""
        limit = Map.MAX_MAP_DIMENSION
        data = {"width": limit + 1, "height": 10, "walls": []}
        with self.assertRaises(ValueError):
            Map.from_dict(data)

    def test_wall_validation_in_from_dict(self):
        """Verify invalid walls are filtered out."""
        width, height = 10, 10
        data = {
            "width": width,
            "height": height,
            "walls": [
                [5, 5],         # Valid
                [-1, 5],        # Invalid: Negative X
                [5, -1],        # Invalid: Negative Y
                [10, 5],        # Invalid: Out of bounds X (width=10, max index 9)
                [5, 10],        # Invalid: Out of bounds Y
                "invalid",      # Invalid: Not a list
                [1],            # Invalid: Too short
                ["a", "b"],     # Invalid: Non-integers
                [1.5, 1.5]      # Invalid: Floats (cast to int 1, 1)
            ]
        }

        m = Map.from_dict(data)

        self.assertTrue(m.is_blocked(5, 5))
        self.assertFalse(m.is_blocked(-1, 5))
        self.assertFalse(m.is_blocked(10, 5))

        # 1.5 -> 1 check
        self.assertTrue(m.is_blocked(1, 1))

        # Count should be 2: (5,5) and (1,1)
        self.assertEqual(len(m.walls), 2)
