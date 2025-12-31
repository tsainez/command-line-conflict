from unittest.mock import patch

import pytest


# Global patch for all tests in this file
@pytest.fixture(autouse=True)
def mock_pygame_mouse():
    with patch("pygame.mouse.set_cursor"):
        yield
