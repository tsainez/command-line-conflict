import pygame

from command_line_conflict import config
from command_line_conflict.campaign_manager import CampaignManager


class MissionSelectScene:
    """Manages the mission selection screen."""

    def __init__(self, game):
        """Initializes the MissionSelectScene.

        Args:
            game: The main game object.
        """
        self.game = game
        self.font = game.font
        self.title_font = pygame.font.Font(None, 60)
        self.option_font = pygame.font.Font(None, 40)

        self.campaign_manager = CampaignManager()
        self.campaign_manager.load_progress()

        self.missions = self.campaign_manager.get_all_missions()
        self.selected_index = 0

    def handle_event(self, event):
        """Handles user input."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % len(self.missions)
            elif event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.missions)
            elif event.key == pygame.K_RETURN:
                mission = self.missions[self.selected_index]
                if self.campaign_manager.is_mission_unlocked(mission["id"]):
                    # Go to briefing
                    # We need to pass the selected mission to the next scene.
                    # SceneManager switch_to typically takes just a name.
                    # We can set a property on the game object or SceneManager,
                    # or better yet, make switch_to accept args.
                    # For now, let's set it on the game object or create the scene instance manually.
                    # However, SceneManager creates scenes.
                    # Let's set `game.current_mission_id` temporarily.

                    self.game.current_mission_id = mission["id"]
                    self.game.scene_manager.switch_to("briefing")
            elif event.key == pygame.K_ESCAPE:
                self.game.scene_manager.switch_to("menu")

    def update(self, dt):
        """Updates the scene."""
        pass

    def draw(self, screen):
        """Draws the scene."""
        screen.fill((0, 0, 0))

        title_text = self.title_font.render("Select Mission", True, (255, 255, 255))
        screen.blit(title_text, (config.SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))

        for i, mission in enumerate(self.missions):
            mission_id = mission["id"]
            is_unlocked = self.campaign_manager.is_mission_unlocked(mission_id)
            is_completed = mission_id in self.campaign_manager.completed_missions

            color = (100, 100, 100) # Locked
            if is_unlocked:
                color = (255, 255, 255) # Available
            if i == self.selected_index:
                color = (255, 255, 0) # Selected

            text_str = mission["title"]
            if is_completed:
                text_str += " [COMPLETED]"
            elif not is_unlocked:
                text_str += " [LOCKED]"

            text = self.option_font.render(text_str, True, color)
            rect = text.get_rect(center=(config.SCREEN_WIDTH // 2, 150 + i * 60))
            screen.blit(text, rect)

        help_text = self.game.font.render("Press RETURN to Start, ESC to Return", True, (150, 150, 150))
        screen.blit(help_text, (config.SCREEN_WIDTH // 2 - help_text.get_width() // 2, config.SCREEN_HEIGHT - 50))
