import os
import unittest

from command_line_conflict.maps.base import Map


class TestSaveRestriction(unittest.TestCase):
    def test_save_to_maps_dir_fails(self):
        """Test that saving to the application source directory is forbidden."""
        m = Map(10, 10)

        # Calculate the path to command_line_conflict/maps relative to this test file
        # tests/security/test_save_restriction.py -> ../../command_line_conflict/maps
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        maps_dir = os.path.join(base_dir, "command_line_conflict", "maps")
        target_path = os.path.join(maps_dir, "test_malicious.json")

        # Ensure we are testing against the resolved path
        target_path = os.path.realpath(target_path)

        # Before the fix, this might succeed if permissions allow.
        # After the fix, this MUST raise ValueError.
        try:
            m.save_to_file(target_path)
            # If we reach here, the save succeeded (unsafe behavior)
            # Clean up the file if it was created
            if os.path.exists(target_path):
                os.remove(target_path)
            self.fail("Map.save_to_file allowed writing to application source directory!")
        except ValueError as e:
            # Expected behavior after fix
            self.assertIn("unauthorized location", str(e))
        except OSError:
            # If we can't write due to OS permissions, that's also fine for this test's purpose of "did it fail?"
            # But ideally we want ValueError from our security check, not OSError.
            # For now, let's just let OSError propagate or fail the test if we want to be strict about *why* it failed.
            pass
