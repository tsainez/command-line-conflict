import functools

import pygame

from command_line_conflict import config

from ..logger import log


class SettingsScene:
    """Manages the settings menu, allowing players to change game options."""

    def __init__(self, game):
        """Initializes the SettingsScene.

        Args:
            game: The main game object, providing access to the screen, font,
                  and scene manager.
        """
        self.game = game
        self.option_font = pygame.font.Font(None, 50)
        self.title_font = pygame.font.Font(None, 74)
        self.settings_options = [
            "Screen Size",
            "Debug Mode",
            "Master Volume",
            "Music Volume",
            "SFX Volume",
            "Back",
        ]
        self.selected_option = 0
        self.option_rects = []
        self.screen_sizes = [(800, 600), (1024, 768), (1280, 720)]
        self.current_screen_size_index = 0
        try:
            self.current_screen_size_index = self.screen_sizes.index((config.SCREEN["width"], config.SCREEN["height"]))
        except ValueError:
            self.current_screen_size_index = 0

    @functools.lru_cache(maxsize=64)
    def _get_text_surface(self, text: str, color: tuple, font_type: str = "option") -> pygame.Surface:
        """Returns a cached surface for the text.

        Args:
            text: The string to render.
            color: The color tuple (R, G, B).
            font_type: 'title', 'help', or 'option'.
        """
        if font_type == "title":
            return self.title_font.render(text, True, color)
        elif font_type == "help":
            return self.game.font.render(text, True, color)
        return self.option_font.render(text, True, color)

    def handle_event(self, event):
        """Handles user input for changing settings.

        Args:
            event: The pygame event to handle.
        """
        if event.type == pygame.MOUSEMOTION:
            hovered = False
            for rect, i in self.option_rects:
                if rect.collidepoint(event.pos):
                    hovered = True
                    self.selected_option = i

            if hovered:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        elif event.type == pygame.MOUSEBUTTONUP:
            for rect, i in self.option_rects:
                if rect.collidepoint(event.pos):
                    self.selected_option = i
                    option_name = self.settings_options[i]
                    if "Volume" in option_name:
                        # Left side decreases, right side increases
                        direction = -1 if event.pos[0] < rect.centerx else 1
                        self._change_volume(option_name, direction)
                    else:
                        self._trigger_option(option_name)

        elif event.type == pygame.KEYDOWN:
            option_name = self.settings_options[self.selected_option]

            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.settings_options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.settings_options)
            elif event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                direction = -1 if event.key == pygame.K_LEFT else 1
                self._change_volume(option_name, direction)

            elif event.key == pygame.K_RETURN:
                self._trigger_option(option_name)

    def _change_volume(self, option_name, direction):
        change = direction * 0.1
        if option_name == "Master Volume":
            config.MASTER_VOLUME = max(0.0, min(1.0, config.MASTER_VOLUME + change))
            self.game.music_manager.refresh_volume()
        elif option_name == "Music Volume":
            config.MUSIC_VOLUME = max(0.0, min(1.0, config.MUSIC_VOLUME + change))
            self.game.music_manager.set_volume(config.MUSIC_VOLUME)
        elif option_name == "SFX Volume":
            config.SOUND_VOLUME = max(0.0, min(1.0, config.SOUND_VOLUME + change))

    def _trigger_option(self, option_name):
        if option_name == "Screen Size":
            self.current_screen_size_index = (self.current_screen_size_index + 1) % len(self.screen_sizes)
            width, height = self.screen_sizes[self.current_screen_size_index]
            config.SCREEN["width"] = width
            config.SCREEN["height"] = height
            self.game.screen = pygame.display.set_mode((width, height))
        elif option_name == "Debug Mode":
            config.DEBUG = not config.DEBUG
            log.info(f"Debug mode set to {config.DEBUG}")
        elif option_name == "Back":
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            self.game.scene_manager.switch_to("menu")

    def update(self, dt):
        """Updates the settings scene. This scene has no dynamic elements.

        Args:
            dt: The time elapsed since the last frame.
        """

    def _get_volume_bar(self, volume):
        """Returns a string representation of a volume bar.

        Args:
            volume: Float between 0.0 and 1.0.

        Returns:
            A string like '[|||||     ] 50%'
        """
        blocks = int(round(volume * 10))
        # Ensure blocks is between 0 and 10
        blocks = max(0, min(10, blocks))
        return f"[{'|' * blocks}{' ' * (10 - blocks)}] {int(round(volume * 100))}%"

    def draw(self, screen):
        """Draws the settings options and title to the screen.

        Args:
            screen: The pygame screen surface to draw on.
        """
        screen.fill((0, 0, 0))

        title_text = self._get_text_surface("Settings", (255, 255, 255), "title")
        title_rect = title_text.get_rect(center=(self.game.screen.get_width() / 2, 100))
        screen.blit(title_text, title_rect)

        self.option_rects.clear()
        for i, option in enumerate(self.settings_options):
            if i == self.selected_option:
                color = (255, 255, 0)
            else:
                color = (255, 255, 255)

            if option == "Screen Size":
                text_to_render = f"{option}: {config.SCREEN['width']}x{config.SCREEN['height']}"
            elif option == "Debug Mode":
                text_to_render = f"{option}: {'On' if config.DEBUG else 'Off'}"
            elif option == "Master Volume":
                text_to_render = f"{option}: {self._get_volume_bar(config.MASTER_VOLUME)}"
            elif option == "Music Volume":
                text_to_render = f"{option}: {self._get_volume_bar(config.MUSIC_VOLUME)}"
            elif option == "SFX Volume":
                text_to_render = f"{option}: {self._get_volume_bar(config.SOUND_VOLUME)}"
            else:
                text_to_render = option

            if i == self.selected_option:
                if "Volume" in option:
                    text_to_render = f"< {text_to_render} >"
                else:
                    text_to_render = f"> {text_to_render} <"

            text = self._get_text_surface(text_to_render, color, "option")
            text_rect = text.get_rect(center=(self.game.screen.get_width() / 2, 250 + i * 60))
            screen.blit(text, text_rect)
            self.option_rects.append((text_rect, i))

        # Helper text for volume controls
        current_option = self.settings_options[self.selected_option]
        if "Volume" in current_option:
            help_text = self._get_text_surface("Use Arrow Keys or Click Left/Right to Adjust", (150, 150, 150), "help")
            help_rect = help_text.get_rect(center=(self.game.screen.get_width() / 2, self.game.screen.get_height() - 50))
            screen.blit(help_text, help_rect)
