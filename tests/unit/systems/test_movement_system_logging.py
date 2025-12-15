import unittest
from unittest.mock import patch, MagicMock

from command_line_conflict.components.movable import Movable
from command_line_conflict.game_state import GameState
from command_line_conflict.maps.simple_map import SimpleMap
from command_line_conflict.systems.movement_system import MovementSystem
from command_line_conflict.factories import create_chassis, create_rover


class TestMovementSystemLogging(unittest.TestCase):
    def setUp(self):
        self.game_state = GameState(SimpleMap())
        self.movement_system = MovementSystem()

    @patch("command_line_conflict.systems.movement_system.log")
    def test_set_target_logs_debug(self, mock_log):
        # Create a unit
        unit_id = create_chassis(self.game_state, x=10, y=10, player_id=1)

        # Move to a valid location
        self.movement_system.set_target(self.game_state, unit_id, 12, 12)

        # Check that debug log was called for setting target
        mock_log.debug.assert_any_call(
            f"Setting target for entity {unit_id} from (10, 10) to (12, 12)"
        )

        # Check that debug log was called for path found
        self.assertTrue(
            any("Path found for entity" in str(call) for call in mock_log.debug.mock_calls)
        )

    @patch("command_line_conflict.systems.movement_system.log")
    def test_set_target_logs_warning_when_no_path(self, mock_log):
        # Create a unit
        unit_id = create_chassis(self.game_state, x=10, y=10, player_id=1)

        # Enclose the unit with walls so no path can be found
        self.game_state.map.add_wall(9, 10)
        self.game_state.map.add_wall(11, 10)
        self.game_state.map.add_wall(10, 9)
        self.game_state.map.add_wall(10, 11)

        # Try to move outside
        self.movement_system.set_target(self.game_state, unit_id, 20, 20)

        # Check warning log
        mock_log.warning.assert_called_with(
            f"No path found for entity {unit_id} from (10, 10) to (20, 20)"
        )

    @patch("command_line_conflict.systems.movement_system.log")
    def test_update_logs_collision_for_non_intelligent(self, mock_log):
        # Create a non-intelligent unit
        unit1_id = create_chassis(self.game_state, x=10, y=10, player_id=1)
        # Create obstacle
        create_chassis(self.game_state, x=10, y=11, player_id=2)

        # Set target to the obstacle
        self.movement_system.set_target(self.game_state, unit1_id, 10, 11)

        # Run update
        self.movement_system.update(self.game_state, dt=0.1)

        # Check if any debug call contains "Collision detected"
        collision_logged = any(
            "Collision detected" in str(call) for call in mock_log.debug.mock_calls
        )
        self.assertTrue(collision_logged, "Should log collision for non-intelligent unit")

    @patch("command_line_conflict.systems.movement_system.log")
    def test_update_logs_intelligent_pathfinding_failure(self, mock_log):
        # Create intelligent unit
        unit_id = create_rover(self.game_state, x=4, y=5, player_id=1)
        movable = self.game_state.get_component(unit_id, Movable)

        # Set target directly (simulating intelligent pathfinding trigger in update)
        movable.target_x = 7.0
        movable.target_y = 5.0
        movable.path = []

        # Surround target with walls so pathfinding fails
        self.game_state.map.add_wall(6, 5)
        self.game_state.map.add_wall(7, 4)
        self.game_state.map.add_wall(7, 6)
        self.game_state.map.add_wall(8, 5)
        # Also block diagonal
        self.game_state.map.add_wall(6, 4)
        self.game_state.map.add_wall(6, 6)
        self.game_state.map.add_wall(8, 4)
        self.game_state.map.add_wall(8, 6)

        # Trigger update
        self.movement_system.update(self.game_state, dt=0.1)

        # Should log failure
        mock_log.warning.assert_any_call(
            f"Intelligent pathfinding failed for entity {unit_id} to (7.0, 5.0)"
        )
