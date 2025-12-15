import os
import sys
from pathlib import Path
from unittest.mock import patch

from command_line_conflict.utils.paths import APP_NAME, get_user_data_dir


def test_get_user_data_dir_linux():
    with patch.object(sys, "platform", "linux"):
        with patch.dict(os.environ, {"XDG_DATA_HOME": "/tmp/xdg_home"}):
            path = get_user_data_dir()
            assert path == Path("/tmp/xdg_home") / APP_NAME

        with patch.dict(os.environ, {}, clear=True):
            # When XDG_DATA_HOME is not set, defaults to ~/.local/share
            # We mock Path.home() to ensure consistent testing if needed,
            # but Path.home() is stable enough for unit tests usually.
            path = get_user_data_dir()
            assert path == Path.home() / ".local" / "share" / APP_NAME


def test_get_user_data_dir_windows():
    with patch.object(sys, "platform", "win32"):
        # Note: on linux/mac host, Path will be posix path, but we can verify string components
        # or rely on pathlib handling.
        # Ideally we'd mock Path too if we want to simulate windows paths on linux,
        # but verifying it uses the env var is enough.
        with patch.dict(os.environ, {"LOCALAPPDATA": "/c/Users/Test/AppData/Local"}):
            path = get_user_data_dir()
            assert str(path) == str(Path("/c/Users/Test/AppData/Local") / APP_NAME)


def test_get_user_data_dir_macos():
    with patch.object(sys, "platform", "darwin"):
        path = get_user_data_dir()
        assert path == Path.home() / "Library" / "Application Support" / APP_NAME
