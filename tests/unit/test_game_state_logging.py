from unittest.mock import MagicMock, patch

import pytest

from command_line_conflict import config
from command_line_conflict.game_state import GameState


class TestGameStateLogging:
    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        # Save original state
        original_debug = config.DEBUG
        yield
        # Restore original state
        config.DEBUG = original_debug

    @patch("command_line_conflict.game_state.log")
    def test_logging_calls(self, mock_log):
        config.DEBUG = True
        mock_map = MagicMock()

        # Test __init__ logging
        game_state = GameState(mock_map)
        mock_log.debug.assert_any_call("GameState initialized")

        # Test create_entity logging
        mock_log.reset_mock()
        entity_id = game_state.create_entity()
        mock_log.debug.assert_called_with(f"Created entity: {entity_id}")

        # Test add_component logging
        class MockComponent:
            pass

        component = MockComponent()
        mock_log.reset_mock()
        game_state.add_component(entity_id, component)
        mock_log.debug.assert_called_with(
            f"Added component MockComponent to entity {entity_id}"
        )

        # Test add_event logging
        event = {"type": "test"}
        mock_log.reset_mock()
        game_state.add_event(event)
        mock_log.debug.assert_called_with(f"Event added: {event}")

        # Test remove_component logging
        mock_log.reset_mock()
        game_state.remove_component(entity_id, MockComponent)
        mock_log.debug.assert_called_with(
            f"Removed component MockComponent from entity {entity_id}"
        )

        # Test remove_entity logging
        mock_log.reset_mock()
        game_state.remove_entity(entity_id)
        mock_log.debug.assert_called_with(f"Removed entity {entity_id}")

    @patch("command_line_conflict.game_state.log")
    def test_no_logging_when_debug_false(self, mock_log):
        config.DEBUG = False
        mock_map = MagicMock()

        game_state = GameState(mock_map)
        mock_log.debug.assert_not_called()

        entity_id = game_state.create_entity()
        mock_log.debug.assert_not_called()
