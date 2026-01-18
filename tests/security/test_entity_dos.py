import pytest

from command_line_conflict import config
from command_line_conflict.game_state import GameState
from command_line_conflict.maps.simple_map import SimpleMap


def test_entity_limit_dos():
    """Verify that we CANNOT create an unlimited number of entities."""
    # Setup
    game_map = SimpleMap()
    game_state = GameState(game_map)

    # We expect to hit the limit (5000 in config)
    # So creating 5001 should raise an error

    # Create up to the limit
    for _ in range(config.MAX_ENTITIES):
        game_state.create_entity()

    # The next one should fail
    with pytest.raises(RuntimeError, match="Maximum entity limit reached"):
        game_state.create_entity()
