import pygame
from command_line_conflict import config


class SettingsScene:
    def __init__(self, game):
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
                elif self.selected_option == 2:
                    self.game.scene_manager.switch_to("menu")

    def update(self, dt):
        pass

    def draw(self, screen):
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
