import pygame

from command_line_conflict import config
from command_line_conflict.campaign_manager import CampaignManager


class BriefingScene:
    """Displays the mission briefing."""

    def __init__(self, game):
        """Initializes the BriefingScene.

        Args:
            game: The main game object.
        """
        self.game = game
        self.font = game.font
        self.title_font = pygame.font.Font(None, 50)
        self.text_font = pygame.font.Font(None, 30)

        self.mission_id = getattr(self.game, "current_mission_id", "mission_1")
        self.campaign_manager = CampaignManager()
        self.mission_data = self.campaign_manager.get_mission(self.mission_id)

        if not self.mission_data:
            # Fallback
            self.mission_data = {
                "title": "Unknown Mission",
                "briefing": "No intelligence data available.",
            }

    def handle_event(self, event):
        """Handles user input."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.game.scene_manager.switch_to("game")
            elif event.key == pygame.K_ESCAPE:
                self.game.scene_manager.switch_to("mission_select")

    def update(self, dt):
        """Updates the scene."""
        pass

    def draw(self, screen):
        """Draws the scene."""
        screen.fill((10, 10, 20))

        # Title
        title_text = self.title_font.render(self.mission_data["title"], True, (0, 255, 0))
        screen.blit(title_text, (50, 50))

        # Briefing Text (Word Wrap)
        text = self.mission_data["briefing"]
        words = text.split(' ')
        lines = []
        current_line = []

        max_width = config.SCREEN_WIDTH - 100

        for word in words:
            current_line.append(word)
            test_surf = self.text_font.render(' '.join(current_line), True, (255, 255, 255))
            if test_surf.get_width() > max_width:
                current_line.pop()
                lines.append(' '.join(current_line))
                current_line = [word]

        lines.append(' '.join(current_line))

        y_offset = 120
        for line in lines:
            line_surf = self.text_font.render(line, True, (200, 255, 200))
            screen.blit(line_surf, (50, y_offset))
            y_offset += 35

        # Unlocks info
        unlocks = self.mission_data.get("unlocks", [])
        if unlocks:
            y_offset += 20
            unlock_text = self.text_font.render(f"Mission Unlocks: {', '.join(unlocks).upper()}", True, (255, 200, 0))
            screen.blit(unlock_text, (50, y_offset))

        # Instructions
        prompt_text = self.game.font.render("Press RETURN to Deploy", True, (0, 255, 0))
        blink_alpha = abs(pygame.time.get_ticks() % 1000 - 500) / 2 # Simple blink effect logic? No, just keep it simple.

        screen.blit(prompt_text, (config.SCREEN_WIDTH - 250, config.SCREEN_HEIGHT - 50))
