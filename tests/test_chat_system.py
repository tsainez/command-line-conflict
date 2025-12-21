# pylint: disable=redefined-outer-name
from unittest.mock import MagicMock

import pygame
import pytest

from command_line_conflict.systems.chat_system import ChatSystem


@pytest.fixture
def chat_system():
    pygame.init()
    screen = MagicMock()
    font = MagicMock()
    # Mock font render to return a surface
    font.render.return_value = MagicMock()
    return ChatSystem(screen, font)


def test_add_message(chat_system):
    chat_system.add_message("Hello World")
    assert len(chat_system.messages) == 1
    assert chat_system.messages[0]["text"] == "Hello World"


def test_max_messages(chat_system):
    chat_system.max_messages = 5
    for i in range(10):
        chat_system.add_message(f"Message {i}")

    assert len(chat_system.messages) == 5
    assert chat_system.messages[-1]["text"] == "Message 9"
    assert chat_system.messages[0]["text"] == "Message 5"


def test_handle_event_activation(chat_system):
    # Ensure it starts inactive
    assert not chat_system.input_active

    # Press Enter to activate
    event = MagicMock()
    event.type = pygame.KEYDOWN
    event.key = pygame.K_RETURN

    consumed = chat_system.handle_event(event)
    assert consumed is True
    assert chat_system.input_active is True


def test_handle_event_typing(chat_system):
    # Activate chat
    chat_system.input_active = True

    # Type 'a'
    event = MagicMock()
    event.type = pygame.KEYDOWN
    event.key = pygame.K_a
    event.unicode = "a"

    chat_system.handle_event(event)
    assert chat_system.input_text == "a"


def test_handle_event_sending(chat_system):
    # Activate and type
    chat_system.input_active = True
    chat_system.input_text = "Hello"

    # Press Enter to send
    event = MagicMock()
    event.type = pygame.KEYDOWN
    event.key = pygame.K_RETURN

    chat_system.handle_event(event)

    assert chat_system.input_active is False
    assert chat_system.input_text == ""
    assert len(chat_system.messages) == 1
    assert chat_system.messages[0]["text"] == "Me: Hello"


def test_handle_event_escape(chat_system):
    # Activate and type
    chat_system.input_active = True
    chat_system.input_text = "Draft"

    # Press Escape to cancel
    event = MagicMock()
    event.type = pygame.KEYDOWN
    event.key = pygame.K_ESCAPE

    chat_system.handle_event(event)

    assert chat_system.input_active is False
    assert chat_system.input_text == ""
    assert len(chat_system.messages) == 0


def test_handle_event_backspace(chat_system):
    # Activate and type
    chat_system.input_active = True
    chat_system.input_text = "Hi"

    # Press Backspace
    event = MagicMock()
    event.type = pygame.KEYDOWN
    event.key = pygame.K_BACKSPACE

    chat_system.handle_event(event)

    assert chat_system.input_text == "H"
