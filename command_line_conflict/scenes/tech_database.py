import pygame

from command_line_conflict import config, factories
from command_line_conflict.campaign_manager import CampaignManager
from command_line_conflict.components.attack import Attack
from command_line_conflict.components.health import Health
from command_line_conflict.components.movable import Movable
from command_line_conflict.components.renderable import Renderable
from command_line_conflict.components.vision import Vision
from command_line_conflict.game_state import GameState
from command_line_conflict.maps.base import Map


class TechDatabaseScene:
    """Displays unlocked units and their statistics."""

    def __init__(self, game):
        """Initializes the TechDatabaseScene.

        Args:
            game: The main game object.
        """
        self.game = game
        self.font = game.font
        self.title_font = pygame.font.Font(None, 60)
        self.header_font = pygame.font.Font(None, 40)
        self.text_font = pygame.font.Font(None, 30)
        self.campaign_manager = CampaignManager()

        # Reload progress to ensure we have latest unlocks
        self.campaign_manager.load_progress()

        self.units = sorted(list(self.campaign_manager.unlocked_units))
        self.selected_index = 0

        # Cache stats to avoid recreating entities constantly
        self.unit_stats = {}
        self._load_unit_stats()

    def _load_unit_stats(self):
        """Creates dummy entities to extract stats."""
        # Create a dummy game state
        dummy_map = Map(10, 10)
        dummy_state = GameState(dummy_map)

        for unit_name in self.units:
            factory_func = factories.UNIT_NAME_TO_FACTORY.get(unit_name)
            if not factory_func:
                continue

            # Create entity off-screen
            try:
                # Some factories require specific args
                if unit_name in ["chassis", "rover", "arachnotron", "observer", "immortal", "extractor"]:
                    entity_id = factory_func(dummy_state, 0, 0, player_id=1, is_human=True)
                elif "factory" in unit_name:
                    entity_id = factory_func(dummy_state, 0, 0, player_id=1, is_human=True)
                else:
                    # Fallback
                    continue

                # Extract components
                stats = {}
                components = dummy_state.entities[entity_id]

                health = components.get(Health)
                if health:
                    stats["HP"] = f"{health.hp}/{health.max_hp}"
                    if hasattr(health, 'health_regen_rate'):
                        stats["Regen"] = f"{health.health_regen_rate}/s"

                attack = components.get(Attack)
                if attack:
                    stats["Damage"] = f"{attack.attack_damage}"
                    stats["Range"] = f"{attack.attack_range}"
                    stats["Speed"] = f"{attack.attack_speed}"

                movable = components.get(Movable)
                if movable:
                    stats["Speed"] = f"{movable.speed}"
                    stats["Flying"] = "Yes" if movable.can_fly else "No"

                vision = components.get(Vision)
                if vision:
                    stats["Vision"] = f"{vision.vision_range}"

                renderable = components.get(Renderable)
                if renderable:
                    stats["Icon"] = renderable.icon
                    stats["Color"] = renderable.color

                self.unit_stats[unit_name] = stats

            except Exception as e:
                print(f"Failed to load stats for {unit_name}: {e}")

    def handle_event(self, event):
        """Handles user input."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % len(self.units)
            elif event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.units)
            elif event.key == pygame.K_ESCAPE:
                self.game.scene_manager.switch_to("menu")

    def update(self, dt):
        """Updates the scene."""
        pass

    def draw(self, screen):
        """Draws the scene."""
        screen.fill((20, 20, 30))

        # Title
        title_text = self.title_font.render("Tech Database", True, (255, 255, 255))
        screen.blit(title_text, (50, 30))

        # Sidebar (Unit List)
        pygame.draw.rect(screen, (40, 40, 50), (30, 100, 250, config.SCREEN_HEIGHT - 130))

        for i, unit_name in enumerate(self.units):
            color = (255, 255, 0) if i == self.selected_index else (200, 200, 200)
            text = self.text_font.render(unit_name.capitalize(), True, color)
            screen.blit(text, (50, 120 + i * 40))

        # Detail View
        if self.units:
            current_unit = self.units[self.selected_index]
            stats = self.unit_stats.get(current_unit, {})

            # Draw Unit Icon (Large)
            icon_char = stats.get("Icon", "?")
            icon_color = stats.get("Color", (255, 255, 255))

            # Hacky way to draw big icon
            big_font = pygame.font.Font(None, 150)
            icon_surf = big_font.render(icon_char, True, icon_color)
            screen.blit(icon_surf, (350, 120))

            # Draw Name
            name_text = self.header_font.render(current_unit.capitalize(), True, (255, 255, 255))
            screen.blit(name_text, (500, 140))

            # Draw Stats
            y_offset = 250
            for key, value in stats.items():
                if key in ["Icon", "Color"]:
                    continue

                stat_text = self.text_font.render(f"{key}: {value}", True, (200, 200, 200))
                screen.blit(stat_text, (350, y_offset))
                y_offset += 40

        # Instructions
        help_text = self.game.font.render("Press ESC to return", True, (100, 100, 100))
        screen.blit(help_text, (config.SCREEN_WIDTH - 200, config.SCREEN_HEIGHT - 30))
