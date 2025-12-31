import os
import pytest
from command_line_conflict.maps.base import Map

def test_save_to_file_path_traversal(tmp_path):
    """Test that saving a map to a path outside allowed directories raises an error."""
    # Create a dummy map
    m = Map(width=10, height=10)

    # Try to save to a file outside the maps directory.
    # tmp_path provided by pytest is outside the repo's map directory and outside the standard user data dir
    # (unless mocked to be the same, which it isn't here).

    malicious_file = tmp_path / "malicious.json"

    # The operation MUST fail with a ValueError containing the security message.
    with pytest.raises(ValueError, match="Security: Cannot save map to unauthorized location"):
        m.save_to_file(str(malicious_file))

    # Double check that the file was NOT created
    assert not os.path.exists(malicious_file)
