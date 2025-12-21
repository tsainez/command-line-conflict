from unittest.mock import MagicMock

import pygame

from command_line_conflict.systems.chat_system import ChatSystem


def test_chat_input_length_limit():
    """
    Test that ChatSystem limits input length to prevent DoS.
    """
    pygame.init()
    screen = MagicMock()
    font = MagicMock()
    font.render.return_value = MagicMock()
    chat = ChatSystem(screen, font)
    chat.input_active = True

    # Simulate typing 300 characters
    long_string = "A" * 300
    for char in long_string:
        event = MagicMock()
        event.type = pygame.KEYDOWN
        event.key = pygame.K_a
        event.unicode = char
        chat.handle_event(event)

    # We expect the input to be truncated to a reasonable limit (e.g. 200)
    assert (
        len(chat.input_text) <= 200
    ), f"Chat input length {len(chat.input_text)} exceeds limit"
