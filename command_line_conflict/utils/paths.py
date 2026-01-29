import json
import os
import sys
import tempfile
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


def atomic_save_json(filepath: str, data: dict) -> None:
    """Saves data to a JSON file atomically to prevent data corruption.

    This method writes data to a temporary file first, flushes it to disk,
    and then atomically moves it to the target location. This ensures that
    in case of a crash or disk failure, the original file is either intact
    or fully replaced, never partially written.

    Args:
        filepath: The path to the file to save to.
        data: The dictionary data to save.

    Raises:
        OSError: If an error occurs during file operations.
    """
    filepath = str(filepath)  # Ensure string if Path passed
    dir_name = os.path.dirname(filepath)
    # Ensure directory exists
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)

    # Create temp file in same directory to ensure atomic move is possible
    # On Windows, os.replace across drives raises WinError 17, so dir must be dir_name
    fd, tmp_path = tempfile.mkstemp(dir=dir_name if dir_name else ".", text=True)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        os.replace(tmp_path, filepath)
    except Exception:
        # Clean up temp file if something went wrong
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        raise
