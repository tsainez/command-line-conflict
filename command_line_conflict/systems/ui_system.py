import pygame
import math

from command_line_conflict.game_state import GameState
from command_line_conflict import config
from command_line_conflict.components.selectable import Selectable
from command_line_conflict.components.health import Health
from command_line_conflict.components.attack import Attack
from command_line_conflict.components.position import Position
from command_line_conflict.components.renderable import Renderable


class UISystem:
    """
    This system is responsible for rendering the UI.
    """

    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.small_font = pygame.font.Font(None, 18)
        self.key_options = [
            "1: Extractor",
            "2: Chassis",
            "3: Rover",
            "4: Arachnotron",
            "5: Observer",
            "6: Immortal",
            "W: Wall",
            "Q: Quit",
        ]

    def draw(self, game_state: GameState) -> None:
        self._draw_key_options()
        selected_entities = self._get_selected_entities(game_state)
        if len(selected_entities) == 1:
            self._draw_single_unit_info(game_state, selected_entities[0])
        elif len(selected_entities) > 1:
            self._draw_multi_unit_info(game_state, selected_entities)

    def _get_selected_entities(self, game_state: GameState) -> list[int]:
        selected_entities = []
        for entity_id, components in game_state.entities.items():
            selectable = components.get(Selectable)
            if selectable and selectable.is_selected:
                selected_entities.append(entity_id)
        return selected_entities

    def _draw_single_unit_info(self, game_state: GameState, entity_id: int) -> None:
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
        components = game_state.entities[entity_id]
        position = components.get(Position)
        attack = components.get(Attack)
        if position and attack and attack.attack_range > 0:
            radius = attack.attack_range * config.GRID_SIZE
            center_x = int(position.x * config.GRID_SIZE + config.GRID_SIZE / 2)
            center_y = int(position.y * config.GRID_SIZE + config.GRID_SIZE / 2)
            self._draw_dotted_circle(
                self.screen, (255, 0, 0), (center_x, center_y), radius, 10
            )

    def _draw_dotted_circle(
        self, surface, color, center, radius, dash_length
    ) -> None:
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
        components = game_state.entities[entity_id]
        position = components.get(Position)
        health = components.get(Health)
        if position and health:
            health_text = f"{int(health.hp)}"
            text = self.small_font.render(health_text, True, (255, 255, 255))
            text_rect = text.get_rect(
                center=(
                    position.x * config.GRID_SIZE + config.GRID_SIZE / 2,
                    position.y * config.GRID_SIZE - 5,
                )
            )
            self.screen.blit(text, text_rect)

    def _draw_multi_unit_info(self, game_state: GameState, entity_ids: list[int]) -> None:
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
