import pygame

from command_line_conflict.campaign_manager import CampaignManager


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
        self.menu_options = ["New Game", "Map Editor", "Options", "Quit"]

        if self.campaign_manager.completed_missions:
            self.menu_options.insert(0, "Continue Campaign")

        self.selected_option = 0
        self.option_rects = []
        self.title_font = pygame.font.Font(None, 74)
        self.option_font = pygame.font.Font(None, 50)

        # Start menu music
        # Assuming the music file is in the root or a music folder
        # For now using a placeholder path
        self.game.music_manager.play("music/menu_theme.ogg")

    def handle_event(self, event):
        """Handles user input for menu navigation.

        Args:
            event: The pygame event to handle.
        """
        if event.type == pygame.MOUSEMOTION:
            for rect, i in self.option_rects:
                if rect.collidepoint(event.pos):
                    self.selected_option = i

        elif event.type == pygame.MOUSEBUTTONUP:
            for rect, i in self.option_rects:
                if rect.collidepoint(event.pos):
                    self._trigger_option(i)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.menu_options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.menu_options)
            elif event.key == pygame.K_RETURN:
                self._trigger_option(self.selected_option)

    def _trigger_option(self, option_index):
        option_text = self.menu_options[option_index]

        if option_text == "Continue Campaign":
            # In the future, this would load the latest save
            # For now, it just starts the game scene, same as New Game
            self.game.scene_manager.switch_to("game")
        elif option_text == "New Game":
            # Ideally reset progress here or start fresh mission
            self.game.scene_manager.switch_to("game")
        elif option_text == "Map Editor":
            self.game.scene_manager.switch_to("editor")
        elif option_text == "Options":
            self.game.scene_manager.switch_to("settings")
        elif option_text == "Quit":
            self.game.running = False

    def update(self, dt):
        """Updates the menu scene. This scene has no dynamic elements.

        Args:
            dt: The time elapsed since the last frame.
        """

    def draw(self, screen):
        """Draws the menu options and title to the screen.

        Args:
            screen: The pygame screen surface to draw on.
        """
        screen.fill((0, 0, 0))

        title_text = self.title_font.render("Command Line Conflict", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.game.screen.get_width() / 2, 100))
        screen.blit(title_text, title_rect)

        self.option_rects.clear()
        for i, option in enumerate(self.menu_options):
            if i == self.selected_option:
                color = (255, 255, 0)
                display_text = f"> {option} <"
            else:
                color = (255, 255, 255)
                display_text = option

            text = self.option_font.render(display_text, True, color)
            text_rect = text.get_rect(center=(self.game.screen.get_width() / 2, 300 + i * 60))
            screen.blit(text, text_rect)
            self.option_rects.append((text_rect, i))
