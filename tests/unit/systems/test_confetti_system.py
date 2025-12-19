from command_line_conflict.factories import create_confetti
from command_line_conflict.game_state import GameState
from command_line_conflict.maps.simple_map import SimpleMap
from command_line_conflict.systems.confetti_system import ConfettiSystem


def test_confetti_system_removes_expired_confetti():
    # Arrange
    game_state = GameState(game_map=SimpleMap())
    confetti_system = ConfettiSystem()
    confetti_id = create_confetti(game_state, 1, 1)

    # Act
    confetti_system.update(game_state, dt=1.0)

    # Assert
    assert confetti_id not in game_state.entities
