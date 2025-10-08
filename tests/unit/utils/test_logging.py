from unittest.mock import patch
from command_line_conflict import config
from command_line_conflict.utils.logging import debug_log

@patch('command_line_conflict.logger.log.info')
def test_debug_log_when_debug_is_true(mock_log_info):
    """Tests that debug_log calls the logger when DEBUG is True."""
    config.DEBUG = True
    debug_log("Test message")
    mock_log_info.assert_called_once_with("Test message")

@patch('command_line_conflict.logger.log.info')
def test_debug_log_when_debug_is_false(mock_log_info):
    """Tests that debug_log does not call the logger when DEBUG is False."""
    config.DEBUG = False
    debug_log("Test message")
    mock_log_info.assert_not_called()