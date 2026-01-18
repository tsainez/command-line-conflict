import os
import pytest
from command_line_conflict.maps.base import Map

def test_save_map_invalid_extension():
    """Verify that saving a map with a non-json extension raises a ValueError."""
    m = Map(width=10, height=10)

    # Try with .py extension
    with pytest.raises(ValueError, match="Map files must have a .json extension"):
        m.save_to_file("test_map.py")

    # Try with .txt extension
    with pytest.raises(ValueError, match="Map files must have a .json extension"):
        m.save_to_file("test_map.txt")

    # Try with no extension
    with pytest.raises(ValueError, match="Map files must have a .json extension"):
        m.save_to_file("test_map")

def test_save_map_valid_extension(tmp_path):
    """Verify that saving a map with .json extension works (within allowed dir logic)."""
    # Note: Map.save_to_file has directory restrictions.
    # To test valid saving, we need to mock the allowed directories or use a valid one.
    # But since we are only testing the extension check here, and the extension check happens
    # BEFORE directory check (or around it), we can at least assert we don't get the extension error.

    # However, if we pass a random path, it might fail on directory check.
    # The message for directory check is "Cannot save to unauthorized location".

    m = Map(width=10, height=10)

    # If we provide a .json extension, it should pass the extension check
    # and fail on the directory check (if path is invalid) OR succeed.

    try:
        m.save_to_file("/tmp/invalid_path/test.json")
    except ValueError as e:
        assert "Map files must have a .json extension" not in str(e)
        # It likely failed with "Cannot save to unauthorized location" or similar
