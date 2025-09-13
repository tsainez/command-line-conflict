from unittest.mock import Mock
from command_line_conflict.systems.corpse_removal_system import CorpseRemovalSystem
from command_line_conflict.components.dead import Dead
from command_line_conflict.game_state import GameState

def test_corpse_removal_system():
    # Arrange
    mock_map = Mock()
    game_state = GameState(game_map=mock_map)
    entity_id = game_state.create_entity()
    game_state.add_component(entity_id, Dead())
    system = CorpseRemovalSystem(corpse_lifetime=5.0)

    # Act
    system.update(game_state, dt=4.0)

    # Assert
    assert entity_id in game_state.entities

    # Act
    system.update(game_state, dt=1.0)

    # Assert
    assert entity_id not in game_state.entities
