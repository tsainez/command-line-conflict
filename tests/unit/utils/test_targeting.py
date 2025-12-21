from unittest.mock import Mock

import pytest

from command_line_conflict.components.player import Player
from command_line_conflict.components.position import Position
from command_line_conflict.components.vision import Vision
from command_line_conflict.game_state import GameState
from command_line_conflict.maps.base import Map
from command_line_conflict.utils.targeting import Targeting


class TestTargeting:
    @pytest.fixture
    def game_state(self):
        game_map = Mock(spec=Map)
        game_map.width = 100
        game_map.height = 100
        return GameState(game_map)

    def create_unit(self, game_state, entity_id, x, y, player_id):  # pylint: disable=too-many-arguments
        game_state.entities[entity_id] = {}
        game_state.add_component(entity_id, Position(x, y))
        game_state.add_component(entity_id, Player(player_id))
        return entity_id

    def test_find_closest_enemy_success(self, game_state):
        # My unit
        my_id = 1
        my_pos = Position(10, 10)
        my_player = Player(1)
        vision = Vision(5)

        # Enemy unit within range (dist 3)
        enemy_id = 2
        self.create_unit(game_state, enemy_id, 13, 10, 2)

        # Add my unit (though find_closest_enemy takes components directly, it might rely on game_state for exclusions)
        self.create_unit(game_state, my_id, 10, 10, 1)

        target = Targeting.find_closest_enemy(my_id, my_pos, my_player, vision, game_state)
        assert target == enemy_id

    def test_find_closest_enemy_ignores_out_of_range(self, game_state):
        my_id = 1
        my_pos = Position(10, 10)
        my_player = Player(1)
        vision = Vision(5)

        # Enemy unit outside range (dist 6)
        enemy_id = 2
        self.create_unit(game_state, enemy_id, 16, 10, 2)

        target = Targeting.find_closest_enemy(my_id, my_pos, my_player, vision, game_state)
        assert target is None

    def test_find_closest_enemy_ignores_friends(self, game_state):
        my_id = 1
        my_pos = Position(10, 10)
        my_player = Player(1)
        vision = Vision(5)

        # Friendly unit within range
        friend_id = 2
        self.create_unit(game_state, friend_id, 12, 10, 1)

        target = Targeting.find_closest_enemy(my_id, my_pos, my_player, vision, game_state)
        assert target is None

    def test_find_closest_enemy_picks_closest(self, game_state):
        my_id = 1
        my_pos = Position(10, 10)
        my_player = Player(1)
        vision = Vision(10)

        # Enemy 1 (dist 4)
        e1 = 2
        self.create_unit(game_state, e1, 14, 10, 2)

        # Enemy 2 (dist 3)
        e2 = 3
        self.create_unit(game_state, e2, 13, 10, 2)

        # Enemy 3 (dist 5)
        e3 = 4
        self.create_unit(game_state, e3, 15, 10, 2)

        target = Targeting.find_closest_enemy(my_id, my_pos, my_player, vision, game_state)
        assert target == e2

    def test_find_closest_enemy_large_coordinates(self, game_state):
        # Test large coordinates to ensure spatial hashing works
        my_id = 1
        my_pos = Position(1000, 1000)
        my_player = Player(1)
        vision = Vision(10)

        enemy_id = 2
        self.create_unit(game_state, enemy_id, 1002, 1002, 2)

        target = Targeting.find_closest_enemy(my_id, my_pos, my_player, vision, game_state)
        assert target == enemy_id
