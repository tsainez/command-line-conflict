import os
import unittest
import shutil
from pathlib import Path

from command_line_conflict.maps.base import Map
from command_line_conflict.utils.paths import get_user_data_dir

class TestMapSerialization(unittest.TestCase):
    def test_to_dict(self):
        m = Map(width=10, height=10)
        m.add_wall(1, 1)
        m.add_wall(2, 2)
        data = m.to_dict()
        self.assertEqual(data["width"], 10)
        self.assertEqual(data["height"], 10)
        # walls is a list of lists or tuples
        # Convert to list of lists for comparison as JSON would serialize it
        walls_list = [list(w) for w in data["walls"]]
        self.assertIn([1, 1], walls_list)
        self.assertIn([2, 2], walls_list)

    def test_from_dict(self):
        data = {"width": 15, "height": 20, "walls": [[5, 5], [6, 6]]}
        m = Map.from_dict(data)
        self.assertEqual(m.width, 15)
        self.assertEqual(m.height, 20)
        self.assertTrue(m.is_blocked(5, 5))
        self.assertTrue(m.is_blocked(6, 6))
        self.assertFalse(m.is_blocked(0, 0))

    def test_save_load(self):
        # Use user data dir for authorized save location
        user_data = get_user_data_dir()
        # Create user data dir if it doesn't exist (mocking environment might not have it)
        try:
             os.makedirs(user_data, exist_ok=True)
        except OSError:
             pass

        filename = os.path.join(user_data, "test_map.json")
        m = Map(width=5, height=5)
        m.add_wall(3, 3)
        m.save_to_file(filename)

        try:
            m2 = Map.load_from_file(filename)
            self.assertEqual(m2.width, 5)
            self.assertEqual(m2.height, 5)
            self.assertTrue(m2.is_blocked(3, 3))
        finally:
            if os.path.exists(filename):
                os.remove(filename)
