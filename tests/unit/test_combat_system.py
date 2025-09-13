import pytest

from command_line_conflict.game_state import GameState
from command_line_conflict.systems.combat_system import CombatSystem
from command_line_conflict.factories import create_rover
from command_line_conflict.components.position import Position
from command_line_conflict.components.vision import Vision
from command_line_conflict.maps.simple_map import SimpleMap


def test_find_closest_enemy_ignores_friendlies():
    # Setup
    game_state = GameState(SimpleMap())
    combat_system = CombatSystem()

    # Create entities
    unit_a_id = create_rover(game_state, 0, 0, player_id=1)
    unit_b_id = create_rover(game_state, 1, 0, player_id=1)  # Friendly
    unit_c_id = create_rover(game_state, 2, 0, player_id=2)  # Enemy

    unit_a_pos = game_state.get_component(unit_a_id, Position)
    unit_a_vision = game_state.get_component(unit_a_id, Vision)

    # Action
    closest_enemy_id = combat_system.find_closest_enemy(
        my_id=unit_a_id,
        my_player_id=1,
        my_pos=unit_a_pos,
        vision=unit_a_vision,
        game_state=game_state,
    )

    # Assertion
    assert closest_enemy_id == unit_c_id
