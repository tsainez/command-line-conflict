import pygame

from ..maps.mission_one import MissionOne
from ..save_game import load_game, save_game
from .game import GameScene


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
        self.menu_options = ["New Campaign", "Continue Campaign", "Options", "Quit"]
        self.selected_option = 0
        self.title_font = pygame.font.Font(None, 74)
        self.option_font = pygame.font.Font(None, 50)

    def handle_event(self, event):
        """Handles user input for menu navigation.
        Args:
            event: The pygame event to handle.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(
                    self.menu_options
                )
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(
                    self.menu_options
                )
            elif event.key == pygame.K_RETURN:
                if self.selected_option == 0:
                    save_game(1)
                    self.game.scene_manager.scenes["game"] = GameScene(
                        self.game, MissionOne()
                    )
                    self.game.scene_manager.switch_to("game")
                elif self.selected_option == 1:
                    mission_number = load_game()
                    if mission_number == 1:
                        self.game.scene_manager.scenes["game"] = GameScene(
                            self.game, MissionOne()
                        )
                    self.game.scene_manager.switch_to("game")
                elif self.selected_option == 2:
                    self.game.scene_manager.switch_to("settings")
                elif self.selected_option == 3:
                    self.game.running = False

    def update(self, dt):
        """Updates the menu scene. This scene has no dynamic elements.
        Args:
            dt: The time elapsed since the last frame.
        """
        pass

    def draw(self, screen):
        """Draws the menu options and title to the screen.
        Args:
            screen: The pygame screen surface to draw on.
        """
        screen.fill((0, 0, 0))

        title_text = self.title_font.render(
            "Command Line Conflict", True, (255, 255, 255)
        )
        title_rect = title_text.get_rect(
            center=(self.game.screen.get_width() / 2, 100)
        )
        screen.blit(title_text, title_rect)

        for i, option in enumerate(self.menu_options):
            if i == self.selected_option:
                color = (255, 255, 0)
            else:
                color = (255, 255, 255)
            text = self.option_font.render(option, True, color)
            text_rect = text.get_rect(
                center=(self.game.screen.get_width() / 2, 300 + i * 60)
            )
            screen.blit(text, text_rect)
