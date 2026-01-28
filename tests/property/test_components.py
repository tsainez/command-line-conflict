from hypothesis import given, strategies as st
from command_line_conflict.components.health import Health
from command_line_conflict.systems.health_system import HealthSystem
from command_line_conflict.game_state import GameState
from command_line_conflict.maps.simple_map import SimpleMap
from unittest.mock import MagicMock

@given(
    hp=st.floats(min_value=0.1, max_value=100.0),
    max_hp=st.floats(min_value=100.0, max_value=200.0),
    regen_rate=st.floats(min_value=0.1, max_value=10.0),
    dt=st.floats(min_value=0.01, max_value=1.0)
)
def test_health_regeneration(hp, max_hp, regen_rate, dt):
    """Verify health regeneration logic."""
    # Setup
    # Ensure hp is less than max_hp for regen to happen
    hp = min(hp, max_hp - 0.1)

    health = Health(hp=hp, max_hp=max_hp, health_regen_rate=regen_rate)

    # Create a minimal GameState with one entity having this health component
    # We need to mock the map as GameState init requires it
    game_state = GameState(SimpleMap())
    entity_id = game_state.create_entity()
    game_state.add_component(entity_id, health)

    system = HealthSystem()
    system.update(game_state, dt)

    # Verification
    expected_hp = min(hp + regen_rate * dt, max_hp)

    # Use approx for float comparison
    assert abs(health.hp - expected_hp) < 1e-6
    assert health.hp <= max_hp

@given(
    hp=st.floats(min_value=-10.0, max_value=0.0),
    max_hp=st.floats(min_value=1.0, max_value=100.0)
)
def test_health_death(hp, max_hp):
    """Verify entity dies when health is <= 0."""
    health = Health(hp=hp, max_hp=max_hp)

    game_state = GameState(SimpleMap())
    entity_id = game_state.create_entity()
    game_state.add_component(entity_id, health)

    system = HealthSystem()
    system.update(game_state, 0.1)

    from command_line_conflict.components.dead import Dead
    assert game_state.get_component(entity_id, Dead) is not None
