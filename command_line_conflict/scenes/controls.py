import pygame

class ControlsScene:
    """Manages the controls menu, allowing players to rebind keys."""

    def __init__(self, game):
        """Initializes the ControlsScene.

        Args:
            game: The main game object.
        """
        self.game = game
        self.font = pygame.font.Font(None, 40)
        self.title_font = pygame.font.Font(None, 74)

        # List of actions to configure
        self.actions = [
            "camera_up", "camera_down", "camera_left", "camera_right",
            "build_rover_factory", "build_arachnotron_factory",
            "hold_position", "pause",
            "toggle_reveal_map", "toggle_god_mode",
            "switch_player", "menu"
        ]

        self.selected_index = 0
        self.rebinding = False

        self.scroll_offset = 0
        self.items_per_page = 8  # Adjust to fit screen height

    def get_action_display_name(self, action):
        """Returns a user-friendly name for an action."""
        return action.replace("_", " ").title()

    def handle_event(self, event):
        """Handles user input for the controls menu."""
        if self.rebinding:
            if event.type == pygame.KEYDOWN:
                # Rebind the selected action
                if event.key != pygame.K_ESCAPE: # Allow cancelling with Escape? Or just rebind?
                    # If Escape is pressed, maybe cancel? But Escape is also bindable ("menu").
                    # Let's assume Escape cancels if it's not the target binding.
                    # But since Escape is "menu", binding it to something else might be tricky.
                    # For now, let's just bind whatever key is pressed.
                    action = self.actions[self.selected_index]
                    self.game.input_manager.set_key(action, event.key)
                self.rebinding = False
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.scene_manager.switch_to("settings")
            elif event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % (len(self.actions) + 1)
            elif event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % (len(self.actions) + 1)
            elif event.key == pygame.K_RETURN:
                if self.selected_index == len(self.actions):
                    # Back button selected
                    self.game.scene_manager.switch_to("settings")
                else:
                    self.rebinding = True

            # Update scroll to keep selected item visible
            if self.selected_index < self.scroll_offset:
                self.scroll_offset = self.selected_index
            elif self.selected_index >= self.scroll_offset + self.items_per_page:
                self.scroll_offset = self.selected_index - self.items_per_page + 1

    def update(self, dt):
        """Updates the controls scene."""
        pass

    def draw(self, screen):
        """Draws the controls menu."""
        screen.fill((0, 0, 0))

        title = self.title_font.render("Controls", True, (255, 255, 255))
        screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, 50))

        start_y = 150
        line_height = 50

        for i in range(self.items_per_page):
            index = self.scroll_offset + i
            if index > len(self.actions):
                break

            y_pos = start_y + i * line_height

            if index == len(self.actions):
                # Back button
                text_str = "Back"
                is_selected = (index == self.selected_index)
            else:
                action = self.actions[index]
                # Ensure input_manager exists (it should be added to game)
                if hasattr(self.game, "input_manager"):
                    key_code = self.game.input_manager.get_key(action)
                    key_name = pygame.key.name(key_code)
                else:
                    key_name = "ERR"

                display_name = self.get_action_display_name(action)

                if self.rebinding and index == self.selected_index:
                    text_str = f"{display_name}: PRESS KEY"
                else:
                    text_str = f"{display_name}: {key_name}"
                is_selected = (index == self.selected_index)

            color = (255, 255, 0) if is_selected else (255, 255, 255)
            text = self.font.render(text_str, True, color)
            rect = text.get_rect(center=(screen.get_width() // 2, y_pos))
            screen.blit(text, rect)
