# pylint: disable=super-init-not-called,redefined-outer-name
from unittest.mock import MagicMock

import pytest

from command_line_conflict.game_state import GameState
from command_line_conflict.maps.base import Map
from command_line_conflict.systems.chat_system import ChatSystem


class MockMap(Map):
    def __init__(self):
        self.width = 10
        self.height = 10
        self.tiles = [[0 for _ in range(10)] for _ in range(10)]


@pytest.fixture
def chat_system():
    screen = MagicMock()
    font = MagicMock()
    return ChatSystem(screen, font)


@pytest.fixture
def game_state():
    return GameState(MockMap())


def test_chat_system_consumes_log_events(chat_system, game_state):
    # Setup log event
    log_event = {"type": "log", "text": "Narrative: Enemy approaching", "color": (255, 255, 0)}
    game_state.add_event(log_event)

    # Update chat system (assuming I update the signature)
    # Since I haven't updated the signature yet, this test would fail if I tried to pass game_state
    # So I will check if update takes game_state, or I will update the code first.
    # But for TDD, I should write the test as I want the code to be.

    # Current signature is update(dt)
    # Desired is update(game_state, dt)

    # Check if we can call it with game_state
    try:
        chat_system.update(game_state, 0.1)
    except TypeError:
        # Expected failure before implementation
        pytest.fail("ChatSystem.update should accept game_state")

    # Check if message was added
    assert len(chat_system.messages) == 1
    assert chat_system.messages[0]["text"] == "Narrative: Enemy approaching"
    assert chat_system.messages[0]["color"] == (255, 255, 0)


def test_chat_system_ignores_other_events(chat_system, game_state):
    sound_event = {"type": "sound", "data": {"name": "bang"}}
    game_state.add_event(sound_event)

    try:
        chat_system.update(game_state, 0.1)
    except TypeError:
        pytest.fail("ChatSystem.update should accept game_state")

    assert len(chat_system.messages) == 0
