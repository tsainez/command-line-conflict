import os
import pygame
from unittest.mock import MagicMock
from command_line_conflict.systems.chat_system import ChatSystem


def test_chat_input_sanitization():
    os.environ["SDL_AUDIODRIVER"] = "dummy"
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    pygame.init()
    screen = MagicMock()
    font = MagicMock()
    font.render.return_value = MagicMock()
    chat = ChatSystem(screen, font)

    chat.input_active = True
    chat.input_text = "<script>alert('xss')</script>"

    event = MagicMock()
    event.type = pygame.KEYDOWN
    event.key = pygame.K_RETURN
    chat.handle_event(event)

    assert len(chat.messages) == 1
    assert (
        "Me: &lt;script&gt;alert(&#x27;xss&#x27;)&lt;/script&gt;" == chat.messages[0]["text"]
    ), f"Expected sanitized output but got {chat.messages[0]['text']}"
