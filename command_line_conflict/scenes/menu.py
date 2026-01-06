import functools
import math

import pygame

from command_line_conflict.campaign_manager import CampaignManager
from command_line_conflict.systems.sound_system import SoundSystem


class MenuScene:
    """Manages the main menu scene, allowing navigation to other scenes."""

    def __init__(self, game):
        """Initializes the MenuScene.

        Args:
            game: The main game object, providing access to the screen, font,
                  and scene manager.
        """
        self.game = game
        self.font = game.font
        self.campaign_manager = CampaignManager()
        self.sound_system = SoundSystem()
        self.menu_options = ["New Game", "Map Editor", "Options", "Quit"]

        if self.campaign_manager.completed_missions:
            self.menu_options.insert(0, "Continue Campaign")

        self.selected_option = 0
        self.option_rects = []
        self.title_font = pygame.font.Font(None, 74)
        self.option_font = pygame.font.Font(None, 50)
        self.time = 0.0

        # Start menu music
        # Assuming the music file is in the root or a music folder
        # For now using a placeholder path
        self.game.music_manager.play("music/menu_theme.ogg")

    @functools.lru_cache(maxsize=32)
    def _get_text_surface(self, text: str, color: tuple, font_type: str = "option") -> pygame.Surface:
        """Returns a cached surface for the text.

        Args:
            text: The string to render.
            color: The color tuple (R, G, B).
            font_type: 'title' or 'option'.
        """
        if font_type == "title":
            return self.title_font.render(text, True, color)
        return self.option_font.render(text, True, color)

    def handle_event(self, event):
        """Handles user input for menu navigation.

        Args:
            event: The pygame event to handle.
        """
        if event.type == pygame.MOUSEMOTION:
            hovered = False
            for rect, i in self.option_rects:
                if rect.collidepoint(event.pos):
                    hovered = True
                    if self.selected_option != i:
                        self.sound_system.play_sound("click_select")
                    self.selected_option = i

            if hovered:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        elif event.type == pygame.MOUSEBUTTONUP:
            for rect, i in self.option_rects:
                if rect.collidepoint(event.pos):
                    self._trigger_option(i)

        elif event.type == pygame.KEYDOWN:
            old_selection = self.selected_option
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.menu_options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.menu_options)
            elif event.key == pygame.K_RETURN:
                self._trigger_option(self.selected_option)

            if self.selected_option != old_selection:
                self.sound_system.play_sound("click_select")

    def _trigger_option(self, option_index):
        option_text = self.menu_options[option_index]

        # Reset cursor before switching scenes
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        if option_text == "Continue Campaign":
            # In the future, this would load the latest save
            # For now, it just starts the game scene, same as New Game
            self.game.scene_manager.switch_to("game", mission_id="mission_1")
        elif option_text == "New Game":
            # Ideally reset progress here or start fresh mission
            self.game.scene_manager.switch_to("game", mission_id="mission_1")
        elif option_text == "Map Editor":
            self.game.scene_manager.switch_to("editor")
        elif option_text == "Options":
            self.game.scene_manager.switch_to("settings")
        elif option_text == "Quit":
            self.game.running = False

    def update(self, dt):
        """Updates the menu scene.

        Args:
            dt: The time elapsed since the last frame.
        """
        self.time += dt

    def draw(self, screen):
        """Draws the menu options and title to the screen.

        Args:
            screen: The pygame screen surface to draw on.
        """
        screen.fill((0, 0, 0))

        title_text = self._get_text_surface("Command Line Conflict", (255, 255, 255), "title")
        title_rect = title_text.get_rect(center=(self.game.screen.get_width() / 2, 100))
        screen.blit(title_text, title_rect)

        # Pulse calculation: varies between 0 and 1
        pulse = (math.sin(self.time * 5) + 1) / 2
        # Interpolate between dim yellow (150, 150, 0) and bright yellow (255, 255, 0)
        yellow_val = 150 + int(105 * pulse)
        pulse_color = (yellow_val, yellow_val, 0)

        self.option_rects.clear()
        for i, option in enumerate(self.menu_options):
            if i == self.selected_option:
                color = pulse_color
                display_text = f"> {option} <"
            else:
                color = (255, 255, 255)
                display_text = option

            text = self._get_text_surface(display_text, color, "option")
            text_rect = text.get_rect(center=(self.game.screen.get_width() / 2, 300 + i * 60))
            screen.blit(text, text_rect)
            self.option_rects.append((text_rect, i))
