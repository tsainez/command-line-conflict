import pygame

from command_line_conflict.scenes.game import GameScene
from command_line_conflict.maps.mission_one import MissionOne

class CampaignMenuScene:
    """A scene for the campaign mission selection."""

    def __init__(self, game):
        """Initializes the CampaignMenuScene.
        Args:
            game: The main game object.
        """
        self.game = game
        self.font = game.font
        self.menu_items = ["Mission 1", "Back"]
        self.selected_item = 0

    def handle_event(self, event):
        """Handles events for the campaign menu.
        Args:
            event: The pygame event to handle.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_item = (self.selected_item - 1) % len(self.menu_items)
            elif event.key == pygame.K_DOWN:
                self.selected_item = (self.selected_item + 1) % len(self.menu_items)
            elif event.key == pygame.K_RETURN:
                if self.selected_item == 0:
                    self.game.scene_manager.scenes["game"] = GameScene(self.game, MissionOne())
                    self.game.scene_manager.switch_to("game")
                elif self.selected_item == 1:
                    self.game.scene_manager.switch_to("menu")

    def update(self, dt):
        """Updates the campaign menu scene.
        Args:
            dt: The time elapsed since the last frame.
        """
        pass

    def draw(self, screen):
        """Draws the campaign menu to the screen.
        Args:
            screen: The pygame screen surface to draw on.
        """
        screen.fill((0, 0, 0))
        title_text = self.font.render("Campaign Missions", True, (255, 255, 255))
        screen.blit(title_text, (20, 20))

        for i, item in enumerate(self.menu_items):
            color = (255, 255, 255)
            if i == self.selected_item:
                color = (255, 0, 0)
            text = self.font.render(item, True, color)
            screen.blit(text, (50, 100 + i * 50))
