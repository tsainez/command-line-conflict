import pytest
from command_line_conflict.components.floating_text import FloatingText
from command_line_conflict.components.position import Position
from command_line_conflict.systems.floating_text_system import \
    FloatingTextSystem


def test_floating_text_update(game_state):
    """Test that the system updates lifetime and position."""
    system = FloatingTextSystem()

    # Create entity
    entity_id = game_state.create_entity()
    game_state.add_component(entity_id, Position(10, 10))
    game_state.add_component(entity_id, FloatingText("Test", (255, 255, 255), 1.0, 1.0))

    # Update - should move up and decrease lifetime
    dt = 0.5
    system.update(game_state, dt)

    components = game_state.entities[entity_id]
    ft = components[FloatingText]
    pos = components[Position]

    assert ft.lifetime == 0.5
    assert pos.y == 9.5  # 10 - (1.0 * 0.5)

    # Update again to kill it
    system.update(game_state, 0.5)

    # Should be removed
    assert entity_id not in game_state.entities

def test_floating_text_spatial_map_update(game_state):
    """Test that moving the text updates the spatial map."""
    system = FloatingTextSystem()

    entity_id = game_state.create_entity()
    game_state.add_component(entity_id, Position(10, 10))
    game_state.add_component(entity_id, FloatingText("Test", (255, 255, 255), 1.0, 1.0))

    assert entity_id in game_state.get_entities_at_position(10, 10)

    # Move enough to change grid cell (default grid size is usually 1, but positions are floats)
    # Rendering uses integer casting. Spatial map uses integer casting.

    # Move from 10.0 to 9.5 -> int(9.5) is 9.
    system.update(game_state, 0.6) # moves 0.6 units up to 9.4

    pos = game_state.get_component(entity_id, Position)
    assert pos.y == 9.4

    # Should be in (10, 9) now
    assert entity_id not in game_state.get_entities_at_position(10, 10)
    assert entity_id in game_state.get_entities_at_position(10, 9)
