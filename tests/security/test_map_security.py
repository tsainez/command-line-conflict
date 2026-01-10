import stat
import unittest
from unittest.mock import MagicMock, patch

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
                [5, 5],  # Valid
                [-1, 5],  # Invalid: Negative X
                [5, -1],  # Invalid: Negative Y
                [10, 5],  # Invalid: Out of bounds X (width=10, max index 9)
                [5, 10],  # Invalid: Out of bounds Y
                "invalid",  # Invalid: Not a list
                [1],  # Invalid: Too short
                ["a", "b"],  # Invalid: Non-integers
                [1.5, 1.5],  # Invalid: Floats (cast to int 1, 1)
            ],
        }

        m = Map.from_dict(data)

        self.assertTrue(m.is_blocked(5, 5))
        self.assertFalse(m.is_blocked(-1, 5))
        self.assertFalse(m.is_blocked(10, 5))

        # 1.5 -> 1 check
        self.assertTrue(m.is_blocked(1, 1))

        # Count should be 2: (5,5) and (1,1)
        self.assertEqual(len(m.walls), 2)

    @patch("command_line_conflict.maps.base.log")
    def test_excessive_walls_truncation(self, mock_log):
        """Verify that excessive wall definitions are truncated."""
        width, height = 5, 5
        max_walls = width * height
        excessive_count = max_walls + 10

        # Create walls list with duplicates (to be valid but excessive)
        walls = [[1, 1] for _ in range(excessive_count)]

        data = {"width": width, "height": height, "walls": walls}

        Map.from_dict(data)

        # Verify log warning
        mock_log.warning.assert_called_once()
        args, _ = mock_log.warning.call_args
        self.assertIn("Too many walls defined", args[0])
        self.assertIn(f"Truncating to {max_walls}", args[0])

    @patch("command_line_conflict.maps.base.open")
    @patch("command_line_conflict.maps.base.os.stat")
    @patch("command_line_conflict.maps.base.os.path.realpath")
    def test_load_from_file_size_limit(self, mock_realpath, mock_stat, mock_open):
        """Verify that loading large map files raises ValueError."""
        # Set size larger than limit (assuming 2MB limit)
        mock_st = MagicMock()
        mock_st.st_size = 5 * 1024 * 1024  # 5MB
        mock_st.st_mode = stat.S_IFREG  # Regular file
        mock_stat.return_value = mock_st

        # We need to make sure the path passes the authorized directory check first
        # otherwise it fails with "unauthorized location" before checking size
        import os

        mock_realpath.return_value = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "../../../command_line_conflict/maps/large_map.json"
        )

        # We also need to mock commonpath logic indirectly by ensuring the paths align
        # But actually, mocking realpath to point to a valid maps dir is easier if we
        # ensure commonpath works.
        # However, Map.load_from_file calls realpath on the input filename.
        # Then it calls realpath on maps_dir.

        # Let's bypass the path check by patching `os.path.commonpath` or ensuring realpath returns a safe path
        with patch("command_line_conflict.maps.base.os.path.commonpath") as mock_commonpath:
            # commonpath returns the first argument to simulate "is inside"
            mock_commonpath.side_effect = lambda paths: paths[0]

            with self.assertRaises(ValueError) as cm:
                Map.load_from_file("large_map.json")

            self.assertIn("exceeds maximum allowed size", str(cm.exception))

        # Ensure open was NOT called
        mock_open.assert_not_called()

    @patch("command_line_conflict.maps.base.open")
    @patch("command_line_conflict.maps.base.os.stat")
    @patch("command_line_conflict.maps.base.os.path.realpath")
    def test_load_from_special_file(self, mock_realpath, mock_stat, mock_open):
        """Verify that loading from special files raises ValueError."""
        mock_st = MagicMock()
        mock_st.st_size = 0
        mock_st.st_mode = stat.S_IFCHR  # Character device
        mock_stat.return_value = mock_st

        # Bypass security check
        with patch("command_line_conflict.maps.base.os.path.commonpath") as mock_commonpath:
            mock_commonpath.side_effect = lambda paths: paths[0]

            with self.assertRaises(ValueError) as cm:
                Map.load_from_file("/dev/zero")

            self.assertIn("must be a regular file", str(cm.exception))

        # Ensure open was NOT called
        mock_open.assert_not_called()
