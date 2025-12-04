import os
import pytest
from unittest.mock import MagicMock, patch

# Mock pygame before importing anything else
with patch.dict(os.environ, {"SDL_VIDEODRIVER": "dummy"}):
    import pygame
    pygame.init()
    pygame.display.set_mode((1, 1))

from command_line_conflict.game_state import GameState
from command_line_conflict.maps import SimpleMap
from command_line_conflict.systems.sound_system import SoundSystem
from command_line_conflict.scenes.game import GameScene

class TestSoundSystem:
    @pytest.fixture
    def game_state(self):
        return GameState(SimpleMap())

    @pytest.fixture
    def sound_system(self):
        return SoundSystem()

    def test_sound_system_initialization(self, sound_system):
        assert sound_system.sounds is not None
        assert "attack" in sound_system.sounds

    def test_play_sound_logs_info(self, sound_system, caplog):
        with caplog.at_level("INFO"):
            sound_system.play_sound("attack")
        assert "[SoundSystem] Playing sound: attack" in caplog.text

    def test_play_sound_missing_logs_warning(self, sound_system, caplog):
        with caplog.at_level("WARNING"):
            sound_system.play_sound("nonexistent")
        assert "[SoundSystem] Sound not found: nonexistent" in caplog.text

    def test_update_processes_events(self, sound_system, game_state, caplog):
        game_state.add_event("sound", {"name": "move"})
        game_state.add_event("other", {"name": "ignore"})

        with caplog.at_level("INFO"):
            sound_system.update(game_state)

        assert "[SoundSystem] Playing sound: move" in caplog.text
        # Ensure sound event is removed
        assert len(game_state.event_queue) == 1
        assert game_state.event_queue[0]["type"] == "other"

class TestIntegration:
    @patch("command_line_conflict.systems.sound_system.SoundSystem.play_sound")
    def test_attack_sound_trigger(self, mock_play_sound):
        # Setup game with mock sound system
        from command_line_conflict.engine import Game
        game = MagicMock(spec=Game)
        game.font = MagicMock()
        game.screen = MagicMock()

        scene = GameScene(game)
        # Manually mock the sound system to spy on it
        scene.sound_system.play_sound = mock_play_sound

        # Setup combat
        # Create attacker and target
        attacker_id = scene.game_state.create_entity()
        from command_line_conflict.components.attack import Attack
        from command_line_conflict.components.position import Position
        from command_line_conflict.components.health import Health
        from command_line_conflict.components.movable import Movable

        scene.game_state.add_component(attacker_id, Position(10, 10))
        scene.game_state.add_component(attacker_id, Attack(10, 1, 1))

        target_id = scene.game_state.create_entity()
        scene.game_state.add_component(target_id, Position(10, 10))
        scene.game_state.add_component(target_id, Health(100, 100))

        # Set target
        attack_comp = scene.game_state.get_component(attacker_id, Attack)
        attack_comp.attack_target = target_id

        # Update combat system (should trigger attack)
        scene.combat_system.update(scene.game_state, 1.0)

        # Verify event was added to queue
        assert any(e["type"] == "sound" and e["data"]["name"] == "attack" for e in scene.game_state.event_queue)

        # Update sound system
        scene.sound_system.update(scene.game_state)

        # Verify play_sound called
        mock_play_sound.assert_called_with("attack")
