import unittest
from command_line_conflict.maps.base import Map

class TestMapExtensionEnforcement(unittest.TestCase):
    def test_save_requires_json_extension(self):
        """Verify that saving a map requires a .json extension."""
        m = Map(10, 10)

        invalid_filenames = [
            "test.py",
            "test.txt",
            "test",
            "test.json.bak",
            "/etc/passwd",
            "script.sh"
        ]

        for fname in invalid_filenames:
            with self.subTest(filename=fname):
                with self.assertRaises(ValueError) as cm:
                    m.save_to_file(fname)
                self.assertEqual(str(cm.exception), "Map files must have a .json extension")

if __name__ == "__main__":
    unittest.main()
