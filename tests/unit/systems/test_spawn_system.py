import unittest
from unittest.mock import MagicMock, patch

from command_line_conflict.game_state import GameState
from command_line_conflict.maps.simple_map import SimpleMap
from command_line_conflict.systems.spawn_system import SpawnSystem


class TestSpawnSystem(unittest.TestCase):
    def setUp(self):
        self.map = SimpleMap()
        self.game_state = GameState(self.map)
        self.spawn_system = SpawnSystem(spawn_interval=5.0)

    @patch("command_line_conflict.factories.create_wildlife")
    def test_update_no_spawn(self, mock_create_wildlife):
        """Test that nothing spawns before the interval."""
        dt = 1.0
        self.spawn_system.update(self.game_state, dt)

        self.assertEqual(self.spawn_system.time_since_last_spawn, 1.0)
        mock_create_wildlife.assert_not_called()

    @patch("command_line_conflict.factories.create_wildlife")
    def test_update_spawn_trigger(self, mock_create_wildlife):
        """Test that spawn is triggered after the interval."""
        # Set time just before spawn
        self.spawn_system.time_since_last_spawn = 4.9
        dt = 0.2

        # Mock map to ensure valid spawn position
        self.game_state.map.width = 10
        self.game_state.map.height = 10
        self.game_state.map.is_walkable = MagicMock(return_value=True)
        self.game_state.get_entities_at_position = MagicMock(return_value=[])

        self.spawn_system.update(self.game_state, dt)

        self.assertEqual(self.spawn_system.time_since_last_spawn, 0.0)
        mock_create_wildlife.assert_called_once()

        # Verify event was added
        self.assertEqual(len(self.game_state.event_queue), 1)
        self.assertEqual(self.game_state.event_queue[0]["type"], "sound")
        self.assertEqual(self.game_state.event_queue[0]["data"]["name"], "spawn_unit")

    @patch("command_line_conflict.factories.create_wildlife")
    def test_spawn_wildlife_no_valid_spot(self, mock_create_wildlife):
        """Test that nothing spawns if no valid spot is found."""
        self.game_state.map.width = 10
        self.game_state.map.height = 10
        # Mock is_walkable to always return False
        self.game_state.map.is_walkable = MagicMock(return_value=False)

        self.spawn_system.spawn_wildlife(self.game_state)

        mock_create_wildlife.assert_not_called()

    @patch("command_line_conflict.factories.create_wildlife")
    def test_spawn_wildlife_occupied(self, mock_create_wildlife):
        """Test that nothing spawns if valid spot is occupied."""
        self.game_state.map.width = 10
        self.game_state.map.height = 10
        self.game_state.map.is_walkable = MagicMock(return_value=True)
        # Mock get_entities_at_position to return entities (occupied)
        self.game_state.get_entities_at_position = MagicMock(return_value=[1])

        self.spawn_system.spawn_wildlife(self.game_state)

        mock_create_wildlife.assert_not_called()


if __name__ == "__main__":
    unittest.main()
