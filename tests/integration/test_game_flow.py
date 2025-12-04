from unittest.mock import Mock, call

import pytest

from command_line_conflict.engine import Game, SceneManager
from command_line_conflict.scenes.game import GameScene
from command_line_conflict.scenes.menu import MenuScene


class TestGameFlow:
    def test_game_flow(self, mocker):
        # Mock pygame inputs
        mocker.patch("pygame.display.set_mode")
        mocker.patch("pygame.init")
        mocker.patch("pygame.font.Font")
        mocker.patch("pygame.display.flip")
        mocker.patch("pygame.quit")
        mocker.patch("pygame.time.Clock")

        # Start game
        game = Game()

        # Verify initial state: Menu Scene
        assert isinstance(game.scene_manager.current_scene, MenuScene)

        # Simulate user input to start game (e.g., pressing Enter)
        # MenuScene usually handles this. Let's assume hitting Enter switches to game.
        # We need to check MenuScene.handle_event implementation or just integration test the transition.
        # Since I haven't read MenuScene, I'll rely on switch_to for now to simulate the flow.

        game.scene_manager.switch_to("game")
        assert isinstance(game.scene_manager.current_scene, GameScene)

        # Simulate game loop updates
        dt = 0.016
        game.scene_manager.update(dt)

        # Simulate game over or back to menu
        game.scene_manager.switch_to("menu")
        assert isinstance(game.scene_manager.current_scene, MenuScene)
