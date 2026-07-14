import functools
import math
from typing import cast

import pygame

from command_line_conflict import config
from command_line_conflict.campaign_manager import CampaignManager
from command_line_conflict.systems.sound_system import SoundSystem
from command_line_conflict.ui.menu_hover_mixin import MenuHoverMixin


class MenuScene(MenuHoverMixin):
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
        self.quit_confirm = False

        if self.campaign_manager.completed_missions:
            self.menu_options.insert(0, "Continue Campaign")

        self.selected_option = 0
        self.help_texts = {
            "Continue Campaign": "Pick up the game in progress, or your saved campaign.",
            "New Game": "Start a new campaign from the beginning.",
            "Map Editor": "Create and edit custom levels.",
            "Options": "Adjust game settings.",
            "Quit": "Exit the game.",
        }
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
            return cast(pygame.Surface, self.title_font.render(text, True, color))
        return cast(pygame.Surface, self.option_font.render(text, True, color))

    def _on_selection_changed(self):
        """Hook for subclasses when the selected option changes."""
        self.quit_confirm = False

    def handle_event(self, event):
        """Handles user input for menu navigation.

        Args:
            event: The pygame event to handle.
        """
        if self.handle_hover_event(event):
            return

        if event.type == pygame.MOUSEBUTTONUP:
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
            elif event.key == pygame.K_ESCAPE:
                self._trigger_option(self.menu_options.index("Quit"))

            if self.selected_option != old_selection:
                self.sound_system.play_sound("click_select")
                self.quit_confirm = False  # Reset confirm if selection changes

    def _trigger_option(self, option_index):
        option_text = self.menu_options[option_index]

        if option_text == "Continue Campaign":
            # reset=False resumes the in-progress match (ESC out of a game
            # freezes the scene rather than discarding it); if there is no
            # resumable match, SceneManager falls back to a fresh mission.
            self.game.scene_manager.switch_to("game", reset=False)
        elif option_text == "New Game":
            self.game.scene_manager.switch_to("game")
        elif option_text == "Map Editor":
            self.game.scene_manager.switch_to("editor")
        elif option_text == "Options":
            self.game.scene_manager.switch_to("settings")
        elif option_text == "Quit":
            if not self.quit_confirm:
                self.quit_confirm = True
                self.sound_system.play_sound("click_select")
            else:
                self.game.running = False
        else:
            self.quit_confirm = False

    def _has_resumable_game(self) -> bool:
        """Whether an in-progress (ESC'd, not finished) game scene exists."""
        scene_manager = getattr(self.game, "scene_manager", None)
        scenes = getattr(scene_manager, "scenes", None)
        if not isinstance(scenes, dict):
            return False
        game_scene = scenes.get("game")
        return (
            game_scene is not None
            and getattr(game_scene, "mission_started", False) is True
            and getattr(game_scene, "mission_over", False) is False
        )

    def _refresh_continue_option(self) -> None:
        """Shows/hides 'Continue Campaign' as the game state changes.

        The option must appear not only when the save file has completed
        missions, but also when the player ESC'd out of a live match — on a
        fresh install that frozen match is otherwise unreachable and the
        player is forced to restart the mission (brutal for playtesting).
        """
        should_show = bool(self.campaign_manager.completed_missions) or self._has_resumable_game()
        has_option = "Continue Campaign" in self.menu_options
        if should_show and not has_option:
            self.menu_options.insert(0, "Continue Campaign")
            self.selected_option = 0
            self.quit_confirm = False
        elif not should_show and has_option:
            self.menu_options.remove("Continue Campaign")
            self.selected_option = 0
            self.quit_confirm = False

    def update(self, dt):
        """Updates the menu scene.

        Args:
            dt: The time elapsed since the last frame.
        """
        self.time += dt
        self._refresh_continue_option()

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
            display_text = option
            color = (255, 255, 255)

            if i == self.selected_option:
                color = pulse_color
                if option == "Quit" and self.quit_confirm:
                    display_text = "> Confirm Quit? <"
                    color = (255, 100, 100)  # Reddish warning color
                else:
                    display_text = f"> {option} <"

            text = self._get_text_surface(display_text, color, "option")
            # 280 + i * 52 keeps the 5-row menu (with Continue Campaign)
            # clear of the help line at SCREEN_HEIGHT - 50 on an 800x600
            # window; 300 + i * 60 used to collide with it.
            text_rect = text.get_rect(center=(self.game.screen.get_width() / 2, 280 + i * 52))
            screen.blit(text, text_rect)
            self.option_rects.append((text_rect, i))

        # Draw helper text for the currently selected option
        current_option = self.menu_options[self.selected_option]
        help_text = self.help_texts.get(current_option, "")
        if help_text:
            help_surf = self.game.font.render(help_text, True, (150, 150, 150))
            help_rect = help_surf.get_rect(center=(self.game.screen.get_width() / 2, self.game.screen.get_height() - 50))
            screen.blit(help_surf, help_rect)

        # Draw game version in bottom-right corner
        version_text = f"v{config.VERSION}"
        version_surf = self.game.font.render(version_text, True, (100, 100, 100))
        version_rect = version_surf.get_rect(
            bottomright=(self.game.screen.get_width() - 10, self.game.screen.get_height() - 10)
        )
        screen.blit(version_surf, version_rect)
