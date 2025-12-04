from unittest.mock import Mock, call

import pytest

from command_line_conflict.components.attack import Attack
from command_line_conflict.components.player import Player
from command_line_conflict.components.position import Position
from command_line_conflict.components.vision import Vision
from command_line_conflict.game_state import GameState
from command_line_conflict.systems.ai_system import AISystem


class TestAISystem:
    def test_ai_acquires_target(self, mocker):
        # Mock Targeting.find_closest_enemy
        mock_find_closest_enemy = mocker.patch(
            "command_line_conflict.utils.targeting.Targeting.find_closest_enemy"
        )

        # Game state and entities
        game_state = GameState(Mock())
        ai_system = AISystem()

        # Entity with all necessary components
        entity_id = 1
        player = Player(1) # AI player
        # Attack(attack_damage, attack_range, attack_speed)
        attack = Attack(attack_damage=10, attack_range=1, attack_speed=1)
        # Vision(vision_range)
        vision = Vision(vision_range=5)
        position = Position(10, 10)

        game_state.entities[entity_id] = {
            Player: player,
            Attack: attack,
            Vision: vision,
            Position: position,
        }

        # Setup mock return for find_closest_enemy
        target_entity_id = 2
        mock_find_closest_enemy.return_value = target_entity_id

        # Run update
        ai_system.update(game_state)

        # Check that find_closest_enemy was called
        mock_find_closest_enemy.assert_called_once_with(
            entity_id, position, player, vision, game_state
        )

        # Check that attack target was set
        assert attack.attack_target == target_entity_id

    def test_ai_does_not_acquire_target_if_already_has_one(self, mocker):
        mock_find_closest_enemy = mocker.patch(
            "command_line_conflict.utils.targeting.Targeting.find_closest_enemy"
        )

        game_state = GameState(Mock())
        ai_system = AISystem()

        entity_id = 1
        attack = Attack(attack_damage=10, attack_range=1, attack_speed=1)
        attack.attack_target = 999 # Already has a target

        game_state.entities[entity_id] = {
            Player: Player(1),
            Attack: attack,
            Vision: Vision(vision_range=5),
            Position: Position(10, 10),
        }

        ai_system.update(game_state)

        # Should not try to find a new target
        mock_find_closest_enemy.assert_not_called()
        assert attack.attack_target == 999

    def test_ai_missing_components(self, mocker):
        mock_find_closest_enemy = mocker.patch(
            "command_line_conflict.utils.targeting.Targeting.find_closest_enemy"
        )

        game_state = GameState(Mock())
        ai_system = AISystem()

        # Entity missing Attack
        game_state.entities[1] = {
            Player: Player(1),
            Vision: Vision(vision_range=5),
            Position: Position(10, 10),
        }

        # Entity missing Player
        game_state.entities[2] = {
            Attack: Attack(attack_damage=10, attack_range=1, attack_speed=1),
            Vision: Vision(vision_range=5),
            Position: Position(10, 10),
        }

        # Entity missing Vision
        game_state.entities[3] = {
            Player: Player(1),
            Attack: Attack(attack_damage=10, attack_range=1, attack_speed=1),
            Position: Position(10, 10),
        }

        ai_system.update(game_state)

        mock_find_closest_enemy.assert_not_called()
