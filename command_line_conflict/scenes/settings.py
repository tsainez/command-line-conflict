import pygame

from command_line_conflict import config

from ..logger import log


class SettingsScene:
    """Manages the settings menu, allowing players to change game options.

    This scene provides an interface for modifying game settings like screen
    resolution and debug mode.

    Attributes:
        game: The main game object, providing access to shared resources.
        option_font: The font used for the settings options.
        title_font: The font used for the scene title.
        settings_options (list[str]): The text for the settings options.
        selected_option (int): The index of the currently selected option.
        screen_sizes (list[tuple[int, int]]): A list of available screen resolutions.
        current_screen_size_index (int): The index of the current screen size.
    """

    def __init__(self, game):
        """Initializes the SettingsScene.

        Args:
            game: The main game object, providing access to the screen, font,
                  and scene manager.
        """
        self.game = game
        self.option_font = pygame.font.Font(None, 50)
        self.title_font = pygame.font.Font(None, 74)
        self.settings_options = ["Screen Size", "Debug Mode", "Back"]
        self.selected_option = 0
        self.screen_sizes = [(800, 600), (1024, 768), (1280, 720)]
        self.current_screen_size_index = 0
        try:
            self.current_screen_size_index = self.screen_sizes.index(
                (config.SCREEN["width"], config.SCREEN["height"])
            )
        except ValueError:
            self.current_screen_size_index = 0

    def handle_event(self, event):
        """Handles user input for changing settings.

        Args:
            event: The pygame event to handle.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(
                    self.settings_options
                )
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(
                    self.settings_options
                )
            elif event.key == pygame.K_RETURN:
                if self.selected_option == 0:
                    self.current_screen_size_index = (
                        self.current_screen_size_index + 1
                    ) % len(self.screen_sizes)
                    width, height = self.screen_sizes[self.current_screen_size_index]
                    config.SCREEN["width"] = width
                    config.SCREEN["height"] = height
                    self.game.screen = pygame.display.set_mode((width, height))
                elif self.selected_option == 1:
                    config.DEBUG = not config.DEBUG
                    log.info(f"Debug mode set to {config.DEBUG}")
                elif self.selected_option == 2:
                    self.game.scene_manager.switch_to("menu")

    def update(self, dt):
        """Updates the settings scene. This scene has no dynamic elements.

        Args:
            dt: The time elapsed since the last frame.
        """

    def draw(self, screen):
        """Draws the settings options and title to the screen.

        Args:
            screen: The pygame screen surface to draw on.
        """
        screen.fill((0, 0, 0))

        title_text = self.title_font.render("Settings", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.game.screen.get_width() / 2, 100))
        screen.blit(title_text, title_rect)

        for i, option in enumerate(self.settings_options):
            if i == self.selected_option:
                color = (255, 255, 0)
            else:
                color = (255, 255, 255)

            if i == 0:
                text_to_render = (
                    f"{option}: {config.SCREEN['width']}x{config.SCREEN['height']}"
                )
            elif i == 1:
                text_to_render = f"{option}: {'On' if config.DEBUG else 'Off'}"
            else:
                text_to_render = option

            text = self.option_font.render(text_to_render, True, color)
            text_rect = text.get_rect(
                center=(self.game.screen.get_width() / 2, 300 + i * 60)
            )
            screen.blit(text, text_rect)
