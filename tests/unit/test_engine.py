from unittest.mock import Mock, call

import pytest

from command_line_conflict.engine import Game, SceneManager
from command_line_conflict.scenes.game import GameScene
from command_line_conflict.scenes.menu import MenuScene
from command_line_conflict.scenes.settings import SettingsScene


class TestSceneManager:
    def test_initialization(self):
        mock_game = Mock()
        manager = SceneManager(mock_game)

        assert manager.game == mock_game
        assert "menu" in manager.scenes
        assert "settings" in manager.scenes
        assert "game" in manager.scenes
        assert isinstance(manager.current_scene, MenuScene)

    def test_switch_to_scene(self):
        mock_game = Mock()
        manager = SceneManager(mock_game)

        # Switch to settings
        manager.switch_to("settings")
        assert isinstance(manager.current_scene, SettingsScene)

        # Switch back to menu
        manager.switch_to("menu")
        assert isinstance(manager.current_scene, MenuScene)

    def test_switch_to_game_resets_scene(self):
        mock_game = Mock()
        manager = SceneManager(mock_game)

        initial_game_scene = manager.scenes["game"]

        # Switch to game
        manager.switch_to("game")
        new_game_scene = manager.scenes["game"]

        # Ensure a new instance is created (as per code implementation)
        assert initial_game_scene is not new_game_scene
        assert isinstance(manager.current_scene, GameScene)

    def test_handle_event(self):
        mock_game = Mock()
        manager = SceneManager(mock_game)
        manager.current_scene = Mock()

        event = Mock()
        manager.handle_event(event)

        manager.current_scene.handle_event.assert_called_once_with(event)

    def test_update(self):
        mock_game = Mock()
        manager = SceneManager(mock_game)
        manager.current_scene = Mock()

        dt = 0.016
        manager.update(dt)

        manager.current_scene.update.assert_called_once_with(dt)

    def test_draw(self):
        mock_game = Mock()
        manager = SceneManager(mock_game)
        manager.current_scene = Mock()

        screen = Mock()
        manager.draw(screen)

        manager.current_scene.draw.assert_called_once_with(screen)


class TestGame:
    def test_initialization(self, mocker):
        mocker.patch("pygame.display.set_mode")
        mocker.patch("pygame.init")
        mocker.patch("pygame.font.Font")

        game = Game()

        assert game.running is True
        assert isinstance(game.scene_manager, SceneManager)
        assert game.screen is not None
        assert game.clock is not None

    def test_run_loop(self, mocker):
        import pygame
        # Mock pygame stuff
        mocker.patch("pygame.display.set_mode")
        mocker.patch("pygame.init")
        mocker.patch("pygame.font.Font")
        mocker.patch("pygame.display.flip")
        mocker.patch("pygame.quit")

        # Mock events: first event is irrelevant, second is QUIT
        mock_event_get = mocker.patch("pygame.event.get")
        quit_event = Mock()
        quit_event.type = pygame.QUIT

        other_event = Mock()
        other_event.type = pygame.USEREVENT

        # Side effect for event.get: first call returns [other_event], second call returns [quit_event]
        # But run loop calls event.get once per tick.
        # We need the loop to run at least once.
        # If we return [quit_event] immediately, it processes it and sets running=False.
        mock_event_get.side_effect = [[other_event], [quit_event]]

        game = Game()

        # Mock scene manager
        game.scene_manager = Mock()

        # Mock clock.tick to avoid waiting
        # We need to mock the clock object itself or its tick method properly.
        # Since game.clock is an instance of pygame.time.Clock, and we can't patch its methods directly if it's a C extension class (which it is),
        # we should have mocked pygame.time.Clock when initializing the game.

        # However, we can also overwrite game.clock with a Mock object since python allows that.
        game.clock = Mock()
        game.clock.tick.return_value = 16

        game.run()

        # Check that scene_manager methods were called
        assert game.scene_manager.handle_event.call_count >= 1
        assert game.scene_manager.update.call_count >= 1
        assert game.scene_manager.draw.call_count >= 1

        assert game.running is False
