import os
import sys
from pathlib import Path

APP_NAME = "command_line_conflict"


def get_user_data_dir() -> Path:
    """Returns the platform-specific user data directory.

    Returns:
        Path: The path to the user data directory for the application.
    """
    if sys.platform == "win32":
        # Windows: %LOCALAPPDATA% or %APPDATA%
        base_path = os.environ.get("LOCALAPPDATA", os.environ.get("APPDATA"))
        if base_path:
            path = Path(base_path)
        else:
            # Fallback if neither is set (unlikely)
            path = Path.home() / "AppData" / "Local"
    elif sys.platform == "darwin":
        # macOS: ~/Library/Application Support
        path = Path.home() / "Library" / "Application Support"
    else:
        # Linux/Unix: $XDG_DATA_HOME or ~/.local/share
        xdg_data = os.environ.get("XDG_DATA_HOME")
        if xdg_data:
            path = Path(xdg_data)
        else:
            path = Path.home() / ".local" / "share"

    return path / APP_NAME
