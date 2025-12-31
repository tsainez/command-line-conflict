from unittest.mock import patch

import pytest


@pytest.fixture(autouse=True)
def mock_pygame_mouse():
    with patch("pygame.mouse.set_cursor"):
        yield
