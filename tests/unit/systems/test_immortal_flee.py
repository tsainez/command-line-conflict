# pylint: disable=redefined-outer-name
"""Tests for the immortal's self-preservation micro.

The immortal flees once HP drops below 20% while an enemy is in sight. The
self-preservation micro must:
  - Drop the attack target so combat doesn't keep firing.
  - Keep the AI from re-acquiring a target while fleeing.
  - Move the unit away from the enemy via the movement system.
"""

import pytest

from command_line_conflict.components.attack import Attack
from command_line_conflict.components.flee import Flee
from command_line_conflict.components.health import Health
from command_line_conflict.components.movable import Movable
from command_line_conflict.components.position import Position
from command_line_conflict.factories import create_immortal, create_rover
from command_line_conflict.game_state import GameState
from command_line_conflict.maps.simple_map import SimpleMap
from command_line_conflict.systems.ai_system import AISystem
from command_line_conflict.systems.combat_system import CombatSystem
from command_line_conflict.systems.flee_system import FleeSystem
from command_line_conflict.systems.movement_system import MovementSystem


@pytest.fixture
def game_state():
    return GameState(SimpleMap())


def _systems():
    return (FleeSystem(), AISystem(), CombatSystem(), MovementSystem())


def test_immortal_does_not_flee_at_full_health(game_state):
    immortal_id = create_immortal(game_state, x=10, y=10, player_id=1, is_human=True)
    create_rover(game_state, x=12, y=10, player_id=2, is_human=False)

    flee_sys, ai, combat, movement = _systems()
    flee_sys.update(game_state, 0.1)
    ai.update(game_state)
    combat.update(game_state, 0.1)
    movement.update(game_state, 0.1)

    flee = game_state.get_component(immortal_id, Flee)
    assert flee.is_fleeing is False


def test_immortal_starts_fleeing_below_threshold(game_state):
    immortal_id = create_immortal(game_state, x=10, y=10, player_id=1, is_human=True)
    create_rover(game_state, x=12, y=10, player_id=2, is_human=False)

    # Drop the immortal under the 20% flee threshold.
    health = game_state.get_component(immortal_id, Health)
    health.hp = int(health.max_hp * 0.1)

    flee_sys, *_ = _systems()
    flee_sys.update(game_state, 0.1)

    flee = game_state.get_component(immortal_id, Flee)
    assert flee.is_fleeing is True


def test_immortal_drops_attack_target_when_fleeing(game_state):
    immortal_id = create_immortal(game_state, x=10, y=10, player_id=1, is_human=True)
    enemy_id = create_rover(game_state, x=12, y=10, player_id=2, is_human=False)

    attack = game_state.get_component(immortal_id, Attack)
    attack.attack_target = enemy_id

    health = game_state.get_component(immortal_id, Health)
    health.hp = int(health.max_hp * 0.1)

    flee_sys, ai, *_ = _systems()
    flee_sys.update(game_state, 0.1)
    ai.update(game_state)  # Must NOT re-acquire while fleeing

    assert attack.attack_target is None


def test_combat_does_not_chase_while_fleeing(game_state):
    """The bug under test: AI re-targets, then combat overrides flee target."""
    immortal_id = create_immortal(game_state, x=10, y=10, player_id=1, is_human=True)
    create_rover(game_state, x=12, y=10, player_id=2, is_human=False)

    health = game_state.get_component(immortal_id, Health)
    health.hp = int(health.max_hp * 0.1)

    flee_sys, ai, combat, movement = _systems()
    # One full pseudo-frame in scene order.
    flee_sys.update(game_state, 0.1)
    ai.update(game_state)
    combat.update(game_state, 0.1)
    movement.update(game_state, 0.1)

    movable = game_state.get_component(immortal_id, Movable)
    pos = game_state.get_component(immortal_id, Position)

    # Flee target should point AWAY from the enemy (negative x direction).
    assert movable.target_x is not None
    assert movable.target_x < 10, f"Expected to flee away (x < 10), got {movable.target_x}"

    # And the immortal should have started moving away.
    assert pos.x <= 10


def test_immortal_stops_fleeing_after_recovery(game_state):
    """Once HP is back up and no enemy in sight, fleeing ends."""
    immortal_id = create_immortal(game_state, x=10, y=10, player_id=1, is_human=True)
    enemy_id = create_rover(game_state, x=12, y=10, player_id=2, is_human=False)

    health = game_state.get_component(immortal_id, Health)
    health.hp = int(health.max_hp * 0.1)

    flee_sys, *_ = _systems()
    flee_sys.update(game_state, 0.1)
    flee = game_state.get_component(immortal_id, Flee)
    assert flee.is_fleeing is True

    # Recover and remove the enemy.
    health.hp = health.max_hp
    game_state.remove_entity(enemy_id)

    flee_sys.update(game_state, 0.1)
    assert flee.is_fleeing is False
