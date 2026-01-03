import unittest
from unittest.mock import MagicMock, patch

import pygame

from command_line_conflict import config
from command_line_conflict.systems.chat_system import ChatSystem


class TestChatSystem(unittest.TestCase):
    def setUp(self):
        self.mock_screen = MagicMock()
        self.mock_font = MagicMock()
        # Mock font.render to return a mock surface
        self.mock_surface = MagicMock()
        self.mock_font.render.return_value = self.mock_surface

        self.chat_system = ChatSystem(self.mock_screen, self.mock_font)

        # Patch pygame.time.get_ticks for predictable timing
        self.patcher_ticks = patch("pygame.time.get_ticks", return_value=1000)
        self.mock_ticks = self.patcher_ticks.start()

    def tearDown(self):
        self.patcher_ticks.stop()

    def test_initialization(self):
        """Test initial state."""
        self.assertEqual(self.chat_system.messages, [])
        self.assertFalse(self.chat_system.input_active)
        self.assertEqual(self.chat_system.input_text, "")
        self.assertFalse(self.chat_system.show_log)

    def test_add_message(self):
        """Test adding messages and queue limit."""
        self.chat_system.add_message("Test Message", (255, 0, 0))

        self.assertEqual(len(self.chat_system.messages), 1)
        self.assertEqual(self.chat_system.messages[0]["text"], "Test Message")
        self.assertEqual(self.chat_system.messages[0]["color"], (255, 0, 0))
        self.assertEqual(self.chat_system.messages[0]["surface"], self.mock_surface)

        # Test exceeding max messages
        self.chat_system.max_messages = 5
        for i in range(10):
            self.chat_system.add_message(f"Msg {i}")

        self.assertEqual(len(self.chat_system.messages), 5)
        # Should contain the last 5 messages (Msg 5 to Msg 9)
        self.assertEqual(self.chat_system.messages[-1]["text"], "Msg 9")
        self.assertEqual(self.chat_system.messages[0]["text"], "Msg 5")

    def test_handle_event_activation(self):
        """Test activating chat with Return key."""
        event = MagicMock(type=pygame.KEYDOWN, key=pygame.K_RETURN)

        # Activating
        consumed = self.chat_system.handle_event(event)
        self.assertTrue(consumed)
        self.assertTrue(self.chat_system.input_active)

        # Deactivating (Sending message)
        self.chat_system.input_text = "Hello"
        consumed = self.chat_system.handle_event(event)
        self.assertTrue(consumed)
        self.assertFalse(self.chat_system.input_active)
        self.assertEqual(self.chat_system.input_text, "")

        # Verify message was added (last message should be our input)
        # Note: messages list might include 'Me: Hello'
        self.assertIn("Me: Hello", self.chat_system.messages[-1]["text"])

    def test_handle_event_typing(self):
        """Test typing into the chat."""
        self.chat_system.input_active = True

        # Type 'A'
        event_a = MagicMock(type=pygame.KEYDOWN, key=pygame.K_a, unicode="A")
        self.chat_system.handle_event(event_a)
        self.assertEqual(self.chat_system.input_text, "A")

        # Type 'B'
        event_b = MagicMock(type=pygame.KEYDOWN, key=pygame.K_b, unicode="B")
        self.chat_system.handle_event(event_b)
        self.assertEqual(self.chat_system.input_text, "AB")

        # Backspace
        event_bs = MagicMock(type=pygame.KEYDOWN, key=pygame.K_BACKSPACE)
        self.chat_system.handle_event(event_bs)
        self.assertEqual(self.chat_system.input_text, "A")

        # Escape
        event_esc = MagicMock(type=pygame.KEYDOWN, key=pygame.K_ESCAPE)
        self.chat_system.handle_event(event_esc)
        self.assertFalse(self.chat_system.input_active)
        self.assertEqual(self.chat_system.input_text, "")

    def test_handle_event_toggle_log(self):
        """Test toggling the persistent log."""
        # Not active input
        self.chat_system.input_active = False

        event = MagicMock(type=pygame.KEYDOWN, key=pygame.K_l)
        consumed = self.chat_system.handle_event(event)

        self.assertTrue(consumed)
        self.assertTrue(self.chat_system.show_log)

        # Toggle back
        self.chat_system.handle_event(event)
        self.assertFalse(self.chat_system.show_log)

    def test_handle_event_ignored(self):
        """Test events that should be ignored."""
        event = MagicMock(type=pygame.MOUSEBUTTONDOWN)
        consumed = self.chat_system.handle_event(event)
        self.assertFalse(consumed)

    def test_update_logs(self):
        """Test processing log events from game state."""
        game_state = MagicMock()
        # Mock event queue with a log event
        game_state.event_queue = [{"type": "log", "text": "System Log", "color": (100, 100, 100)}]

        self.chat_system.update(game_state, 0.1)

        self.assertEqual(len(self.chat_system.messages), 1)
        self.assertEqual(self.chat_system.messages[0]["text"], "System Log")

    def test_draw_conditions(self):
        """Test when chat should be drawn."""
        # 1. No history, input inactive -> Should not draw (mostly)

        # Mock time to be long after last message
        self.mock_ticks.return_value = 10000
        self.chat_system.last_message_time = 1000
        self.chat_system.chat_history_duration = 5000

        self.chat_system.draw()
        self.mock_screen.blit.assert_not_called()

        # 2. Input active -> Should draw
        self.chat_system.input_active = True
        self.chat_system.draw()
        self.assertTrue(self.mock_screen.blit.called)
        self.mock_screen.blit.reset_mock()

        # 3. Recent message -> Should draw
        self.chat_system.input_active = False
        # Need to ensure current time is close to last_message_time
        # last_message_time = 1000
        # current_time must be < 1000 + 5000 = 6000
        self.mock_ticks.return_value = 2000
        self.chat_system.last_message_time = 1000
        self.chat_system.messages.append(
            {
                "text": "Test",
                "color": (255, 255, 255),
                "time": 1000,
                "surface": self.mock_surface,
                "shadow_surface": self.mock_surface,
            }
        )  # Need a message to trigger the loop in draw

        self.chat_system.draw()
        self.assertTrue(self.mock_screen.blit.called)

    def test_input_length_limit(self):
        """Test that input is limited by MAX_CHAT_INPUT_LENGTH."""
        self.chat_system.input_active = True
        limit = config.MAX_CHAT_INPUT_LENGTH

        # Fill buffer
        self.chat_system.input_text = "A" * limit

        # Try to add one more
        event = MagicMock(type=pygame.KEYDOWN, key=pygame.K_b, unicode="B")
        self.chat_system.handle_event(event)

        self.assertEqual(len(self.chat_system.input_text), limit)
        self.assertEqual(self.chat_system.input_text, "A" * limit)


if __name__ == "__main__":
    unittest.main()
