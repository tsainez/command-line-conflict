import os
import pygame
from unittest.mock import patch
from command_line_conflict.engine import Game

@patch("pygame.display.flip")
def test_smoke_test(mock_flip):
    """Tests that the game can be initialized and run for a few frames."""
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    pygame.init()
    pygame.display.set_mode((1, 1))
    game = Game()
    for _ in range(10):
        game.tick()
    game.running = False
    pygame.quit()
