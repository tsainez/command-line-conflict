from unittest.mock import MagicMock

from command_line_conflict.components.dead import Dead
from command_line_conflict.components.resource_deposit import ResourceDeposit
from command_line_conflict.game_state import GameState


class TestGameStateObstacles:
    def test_get_blocking_obstacles(self):
        mock_map = MagicMock()
        game_state = GameState(mock_map)

        # Setup spatial map with various entities
        game_state.spatial_map = {
            (0, 0): {1},  # 1 is Dead -> no blocking
            (1, 1): {2},  # 2 is ResourceDeposit -> no blocking
            (2, 2): {3},  # 3 is neither -> blocking
            (3, 3): {4, 5},  # 4 is Dead, 5 is neither -> blocking
            (4, 4): {6, 7},  # 6 is Dead, 7 is ResourceDeposit -> no blocking
        }

        # Mock get_component to simulate entity properties
        def mock_get_component(eid, component_type):
            components = {
                1: {Dead: MagicMock()},
                2: {ResourceDeposit: MagicMock()},
                3: {},
                4: {Dead: MagicMock()},
                5: {},
                6: {Dead: MagicMock()},
                7: {ResourceDeposit: MagicMock()},
            }
            return components.get(eid, {}).get(component_type, None)

        game_state.get_component = mock_get_component

        result = game_state.get_blocking_obstacles()

        assert result == {(2, 2): {3}, (3, 3): {4, 5}}
