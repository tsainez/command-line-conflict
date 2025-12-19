import pygame

from command_line_conflict import config


class ChatSystem:
    """Handles the in-game chat system, including message history and input."""

    def __init__(self, screen, font):
        """Initializes the ChatSystem.

        Args:
            screen: The pygame screen surface to draw on.
            font: The pygame font to use for rendering text.
        """
        self.screen = screen
        self.font = font
        self.messages = []  # List of (text, color) tuples
        self.input_active = False
        self.input_text = ""
        self.max_messages = 10
        self.chat_history_duration = 5000  # Milliseconds to show chat history
        self.last_message_time = 0
        self.cursor_blink_timer = 0
        self.cursor_visible = True

    def add_message(self, text: str, color: tuple[int, int, int] = (255, 255, 255)):
        """Adds a message to the chat history.

        Args:
            text: The message text.
            color: The color of the text (RGB tuple).
        """
        self.messages.append(
            {"text": text, "color": color, "time": pygame.time.get_ticks()}
        )
        if len(self.messages) > self.max_messages:
            self.messages.pop(0)
        self.last_message_time = pygame.time.get_ticks()

    def handle_event(self, event) -> bool:
        """Handles user input for the chat system.

        Args:
            event: The pygame event to handle.

        Returns:
            True if the event was consumed by the chat system, False otherwise.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if self.input_active:
                    if self.input_text.strip():
                        # In the future, this would send the message to the server
                        # For now, we just echo it locally
                        self.add_message(f"Me: {self.input_text}", (0, 255, 255))
                    self.input_text = ""
                    self.input_active = False
                else:
                    self.input_active = True
                    self.last_message_time = (
                        pygame.time.get_ticks()
                    )  # Keep history visible while typing
                return True

            if self.input_active:
                if event.key == pygame.K_ESCAPE:
                    self.input_active = False
                    self.input_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]
                else:
                    # Filter out non-printable characters if necessary,
                    # but event.unicode usually handles it.
                    if (
                        len(event.unicode) > 0
                        and event.unicode.isprintable()
                        and len(self.input_text) < config.MAX_CHAT_INPUT_LENGTH
                    ):
                        self.input_text += event.unicode
                return True

        return False

    def update(self, dt: float):
        """Updates the chat system state.

        Args:
            dt: Time elapsed since last frame.
        """
        if self.input_active:
            self.cursor_blink_timer += dt
            if self.cursor_blink_timer >= 0.5:
                self.cursor_visible = not self.cursor_visible
                self.cursor_blink_timer = 0
            # Keep history visible while typing
            self.last_message_time = pygame.time.get_ticks()

    def draw(self):
        """Draws the chat overlay and input box."""
        current_time = pygame.time.get_ticks()

        # Determine if we should show history
        show_history = self.input_active or (
            current_time - self.last_message_time < self.chat_history_duration
        )

        if not show_history and not self.input_active:
            return

        chat_bottom = config.SCREEN_HEIGHT - 120
        line_height = 20

        # Draw messages
        if show_history:
            for i, msg in enumerate(reversed(self.messages)):
                text_surface = self.font.render(msg["text"], True, msg["color"])
                # Add a slight shadow/outline for better visibility
                shadow_surface = self.font.render(msg["text"], True, (0, 0, 0))

                y_pos = chat_bottom - (i + 1) * line_height
                if self.input_active:
                    y_pos -= line_height + 5  # Make room for input box

                self.screen.blit(shadow_surface, (12, y_pos + 2))
                self.screen.blit(text_surface, (10, y_pos))

        # Draw input box
        if self.input_active:
            input_y = chat_bottom - line_height

            # Draw background for input
            input_bg_rect = pygame.Rect(5, input_y - 2, 400, line_height + 4)
            pygame.draw.rect(self.screen, (0, 0, 0, 180), input_bg_rect)
            pygame.draw.rect(self.screen, (100, 100, 100), input_bg_rect, 1)

            # Draw text
            display_text = f"Chat: {self.input_text}"
            if self.cursor_visible:
                display_text += "_"

            text_surface = self.font.render(display_text, True, (255, 255, 255))
            self.screen.blit(text_surface, (10, input_y))
