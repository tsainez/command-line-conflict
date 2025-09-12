import pygame


class MenuScene:
    def __init__(self, game):
        self.game = game
        self.font = game.font
        self.menu_options = ["New Game", "Options", "Quit"]
        self.selected_option = 0
        self.title_font = pygame.font.Font(None, 74)
        self.option_font = pygame.font.Font(None, 50)

    def handle_event(self, event):
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
                    self.game.scene_manager.switch_to("game")
                elif self.selected_option == 1:
                    self.game.scene_manager.switch_to("settings")
                elif self.selected_option == 2:
                    self.game.running = False

    def update(self, dt):
        pass

    def draw(self, screen):
        screen.fill((0, 0, 0))

        title_text = self.title_font.render(
            "Command Line Conflict", True, (255, 255, 255)
        )
        title_rect = title_text.get_rect(center=(self.game.screen.get_width() / 2, 100))
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
