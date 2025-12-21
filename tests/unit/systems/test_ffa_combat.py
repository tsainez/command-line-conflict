from unittest.mock import MagicMock

# pylint: disable=redefined-outer-name
import pytest

from command_line_conflict.components.attack import Attack
from command_line_conflict.components.player import Player
from command_line_conflict.components.position import Position
from command_line_conflict.components.vision import Vision
from command_line_conflict.game_state import GameState
from command_line_conflict.maps.base import Map
from command_line_conflict.systems.ai_system import AISystem


@pytest.fixture
def game_state():
    return GameState(MagicMock(spec=Map))


@pytest.fixture
def ai_system():
    return AISystem()


def create_unit(game_state, entity_id, player_id, x, y):
    # Use add_component to ensure spatial_map is populated
    game_state.entities[entity_id] = {}
    game_state.add_component(entity_id, Player(player_id=player_id))
    game_state.add_component(entity_id, Position(x, y))
    game_state.add_component(entity_id, Attack(attack_damage=10, attack_range=5, attack_speed=1))
    game_state.add_component(entity_id, Vision(vision_range=10))


def test_ffa_combat_auto_targeting(game_state, ai_system):
    """Test that units from different players automatically target each other."""
    # Create Unit 1 (Player 1) at (10, 10)
    create_unit(game_state, 1, 1, 10, 10)

    # Create Unit 2 (Player 2) at (12, 10) - within range
    create_unit(game_state, 2, 2, 12, 10)

    # Create Unit 3 (Player 3) at (10, 12) - within range
    create_unit(game_state, 3, 3, 10, 12)

    ai_system.update(game_state)

    # Unit 1 should target either 2 or 3 (closest is equal distance sqrt(4)=2)
    unit1_attack = game_state.get_component(1, Attack)
    assert unit1_attack.attack_target in [2, 3]

    # Unit 2 should target 1 or 3
    unit2_attack = game_state.get_component(2, Attack)
    assert unit2_attack.attack_target in [1, 3]

    # Unit 3 should target 1 or 2
    unit3_attack = game_state.get_component(3, Attack)
    assert unit3_attack.attack_target in [1, 2]


def test_neutral_units_passive(game_state, ai_system):
    """Test that neutral units (Player 0) do not auto-acquire targets."""
    # Create Neutral Unit (Player 0)
    create_unit(game_state, 1, 0, 10, 10)

    # Create Player Unit (Player 1) nearby
    create_unit(game_state, 2, 1, 12, 10)

    ai_system.update(game_state)

    # Neutral unit should NOT have a target
    neutral_attack = game_state.get_component(1, Attack)
    assert neutral_attack.attack_target is None

    # Player unit SHOULD target the neutral unit (unless targeting logic excludes neutrals, currently it does not)
    player_attack = game_state.get_component(2, Attack)
    assert player_attack.attack_target == 1
