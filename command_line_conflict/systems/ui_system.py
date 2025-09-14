import pygame
import math

from command_line_conflict.game_state import GameState
from command_line_conflict import config
from command_line_conflict.components.selectable import Selectable
from command_line_conflict.components.health import Health
from command_line_conflict.components.attack import Attack
from command_line_conflict.components.position import Position
from command_line_conflict.components.renderable import Renderable


from command_line_conflict.camera import Camera


class UISystem:
    """Handles rendering the user interface, including unit info and key options."""

    def __init__(self, screen, font, camera: Camera):
        """Initializes the UISystem.

        Args:
            screen: The pygame screen surface to draw on.
            font: The main pygame font to use for rendering text.
            camera: The camera object for view/zoom.
        """
        self.screen = screen
        self.font = font
        self.camera = camera
        self.small_font = pygame.font.Font(None, 18)
        self.key_options = [
            "1: Extractor",
            "2: Chassis",
            "3: Rover",
            "4: Arachnotron",
            "5: Observer",
            "6: Immortal",
            "W: Wall",
        ]

    def draw(self, game_state: GameState, paused: bool) -> None:
        """Draws the main UI, including selected unit info and key options.

        Args:
            game_state: The current state of the game.
        """
        self._draw_key_options()
        selected_entities = self._get_selected_entities(game_state)
        if len(selected_entities) == 1:
            self._draw_single_unit_info(game_state, selected_entities[0])
        elif len(selected_entities) > 1:
            self._draw_multi_unit_info(game_state, selected_entities)

        if paused:
            self._draw_paused_message()

    def _get_selected_entities(self, game_state: GameState) -> list[int]:
        """Gets a list of all currently selected entity IDs.

        Args:
            game_state: The current state of the game.

        Returns:
            A list of entity IDs for all selected entities.
        """
        selected_entities = []
        for entity_id, components in game_state.entities.items():
            selectable = components.get(Selectable)
            if selectable and selectable.is_selected:
                selected_entities.append(entity_id)
        return selected_entities

    def _draw_single_unit_info(self, game_state: GameState, entity_id: int) -> None:
        """Draws the detailed information panel for a single selected unit.

        Args:
            game_state: The current state of the game.
            entity_id: The ID of the selected entity.
        """
        components = game_state.entities[entity_id]
        health = components.get(Health)
        attack = components.get(Attack)
        renderable = components.get(Renderable)

        panel_x_offset = 10
        panel_y = config.SCREEN_HEIGHT - 90

        if renderable:
            text = self.font.render(f"Unit: {renderable.icon}", True, (255, 255, 255))
            self.screen.blit(text, (panel_x_offset, panel_y))
            panel_y += 20

        if health:
            health_text = f"Health: {int(health.hp)} / {health.max_hp}"
            text = self.font.render(health_text, True, (255, 255, 255))
            self.screen.blit(text, (panel_x_offset, panel_y))
            panel_y += 20

        if attack:
            attack_text = f"Attack: {attack.attack_damage} (Range: {attack.attack_range})"
            text = self.font.render(attack_text, True, (255, 255, 255))
            self.screen.blit(text, (panel_x_offset, panel_y))

        self._draw_attack_range(game_state, entity_id)
        self._draw_unit_health_text(game_state, entity_id)

    def _draw_attack_range(self, game_state: GameState, entity_id: int) -> None:
        """Draws a circle indicating the attack range of a unit.

        Args:
            game_state: The current state of the game.
            entity_id: The ID of the entity.
        """
        components = game_state.entities[entity_id]
        position = components.get(Position)
        attack = components.get(Attack)
        if position and attack and attack.attack_range > 0:
            radius = attack.attack_range * config.GRID_SIZE * self.camera.zoom
            center_x = int(
                (position.x - self.camera.x) * config.GRID_SIZE * self.camera.zoom
                + config.GRID_SIZE * self.camera.zoom / 2
            )
            center_y = int(
                (position.y - self.camera.y) * config.GRID_SIZE * self.camera.zoom
                + config.GRID_SIZE * self.camera.zoom / 2
            )
            self._draw_dotted_circle(
                self.screen, (255, 0, 0), (center_x, center_y), radius, 10
            )

    def _draw_dotted_circle(
        self, surface, color, center, radius, dash_length
    ) -> None:
        """Draws a dotted circle on a surface.

        Args:
            surface: The pygame surface to draw on.
            color: The color of the circle.
            center: The (x, y) coordinates of the circle's center.
            radius: The radius of the circle.
            dash_length: The length of each dash in the circle.
        """
        num_dashes = 30
        for i in range(num_dashes):
            angle = 2 * math.pi * i / num_dashes
            start_angle = angle
            end_angle = angle + 2 * math.pi / (2 * num_dashes)
            start_pos = (
                center[0] + radius * math.cos(start_angle),
                center[1] + radius * math.sin(start_angle),
            )
            end_pos = (
                center[0] + radius * math.cos(end_angle),
                center[1] + radius * math.sin(end_angle),
            )
            pygame.draw.line(surface, color, start_pos, end_pos, 1)

    def _draw_unit_health_text(self, game_state: GameState, entity_id: int) -> None:
        """Draws the current health of a unit above its icon.

        Args:
            game_state: The current state of the game.
            entity_id: The ID of the entity.
        """
        components = game_state.entities[entity_id]
        position = components.get(Position)
        health = components.get(Health)
        if position and health:
            health_text = f"{int(health.hp)}"
            text = self.small_font.render(health_text, True, (255, 255, 255))
            grid_size = config.GRID_SIZE * self.camera.zoom
            center_x = (
                (position.x - self.camera.x) * config.GRID_SIZE * self.camera.zoom
                + grid_size / 2
            )
            center_y = (
                (position.y - self.camera.y) * config.GRID_SIZE * self.camera.zoom
                - 5 * self.camera.zoom
            )
            text_rect = text.get_rect(center=(center_x, center_y))
            self.screen.blit(text, text_rect)

    def _draw_multi_unit_info(self, game_state: GameState, entity_ids: list[int]) -> None:
        """Draws the information panel for multiple selected units.

        This shows the total number of units and their combined health.

        Args:
            game_state: The current state of the game.
            entity_ids: A list of IDs for the selected entities.
        """
        total_health = 0
        max_health = 0
        for entity_id in entity_ids:
            health = game_state.get_component(entity_id, Health)
            if health:
                total_health += health.hp
                max_health += health.max_hp

        panel_x_offset = 10
        panel_y = config.SCREEN_HEIGHT - 90

        count_text = f"Selected Units: {len(entity_ids)}"
        text = self.font.render(count_text, True, (255, 255, 255))
        self.screen.blit(text, (panel_x_offset, panel_y))
        panel_y += 20

        health_text = f"Total Health: {int(total_health)} / {max_health}"
        text = self.font.render(health_text, True, (255, 255, 255))
        self.screen.blit(text, (panel_x_offset, panel_y))

    def _draw_key_options(self) -> None:
        """Draws the panel at the bottom of the screen showing key bindings."""
        panel_height = 100
        panel_y = config.SCREEN_HEIGHT - panel_height
        panel_rect = pygame.Rect(0, panel_y, config.SCREEN_WIDTH, panel_height)
        overlay = pygame.Surface(panel_rect.size, pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.screen.blit(overlay, panel_rect.topleft)
        pygame.draw.rect(self.screen, (255, 255, 255), panel_rect, 1)

        x_offset = 410
        y_offset = panel_y + 10
        column_width = 150
        row_height = 20
        items_per_row = 2

        for i, option in enumerate(self.key_options):
            col = i % items_per_row
            row = i // items_per_row

            x_pos = x_offset + col * column_width
            y_pos = y_offset + row * row_height

            text = self.font.render(option, True, (255, 255, 255))
            self.screen.blit(text, (x_pos, y_pos))

    def _draw_paused_message(self) -> None:
        font = pygame.font.Font(None, 74)
        text = font.render("Paused", True, (255, 255, 255))
        text_rect = text.get_rect(
            center=(config.SCREEN_WIDTH / 2, config.SCREEN_HEIGHT / 2)
        )
        self.screen.blit(text, text_rect)
