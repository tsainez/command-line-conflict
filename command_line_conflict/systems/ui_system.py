import math

import pygame

from command_line_conflict import config
from command_line_conflict.camera import Camera
from command_line_conflict.components.attack import Attack
from command_line_conflict.components.detection import Detection
from command_line_conflict.components.health import Health
from command_line_conflict.components.position import Position
from command_line_conflict.components.renderable import Renderable
from command_line_conflict.components.selectable import Selectable
from command_line_conflict.game_state import GameState
from command_line_conflict.logger import log


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
        self.cheats = {}
        self.small_font = pygame.font.Font(None, 18)
        self.key_options = [
            "1: Extractor",
            "2: Chassis",
            "3: Rover",
            "4: Arachnotron",
            "5: Observer",
            "6: Immortal",
            "Arrow Keys: Move Camera",
        ]

        # State tracking for logging
        self.last_selected_count = -1
        self.last_active_cheats_count = -1

        # Pre-create the pause overlay
        self.pause_overlay = pygame.Surface(
            (config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.SRCALPHA
        )
        self.pause_overlay.fill((0, 0, 0, 150))

        log.debug("UISystem initialized")

    def draw(self, game_state: GameState, paused: bool, current_player_id: int = 1) -> None:
        """Draws the main UI, including selected unit info and key options.

        Args:
            game_state: The current state of the game.
            paused: Whether the game is paused.
            current_player_id: The ID of the player currently controlling the game.
        """
        self._draw_key_options()
        self._draw_player_indicator(current_player_id)

        if self.cheats:
            self._draw_active_cheats(self.cheats)

            # Log changes in active cheats
            active_cheats_count = sum(1 for v in self.cheats.values() if v)
            if active_cheats_count != self.last_active_cheats_count:
                log.debug(f"UI: Active cheats count changed to {active_cheats_count}")
                self.last_active_cheats_count = active_cheats_count

        selected_entities = self._get_selected_entities(game_state)

        # Log changes in selection
        if len(selected_entities) != self.last_selected_count:
            log.debug(f"UI: Selection changed. Count: {len(selected_entities)}")
            self.last_selected_count = len(selected_entities)

        if len(selected_entities) == 1:
            self._draw_single_unit_info(game_state, selected_entities[0])
        elif len(selected_entities) > 1:
            self._draw_multi_unit_info(game_state, selected_entities)
            self._draw_aggregate_detection_range(game_state, selected_entities)
            self._draw_aggregate_attack_range(game_state, selected_entities)

        if paused:
            self._draw_paused_message()

    def _draw_player_indicator(self, current_player_id: int) -> None:
        """Draws a visual indicator for the current player.

        Args:
            current_player_id: The ID of the player currently controlling the game.
        """
        indicator_size = 20
        padding = 10
        # Position at the bottom left, above the key options or next to them
        x = padding
        y = config.SCREEN_HEIGHT - indicator_size - padding

        color = (0, 255, 0) if current_player_id == 1 else (255, 0, 0)

        rect = pygame.Rect(x, y, indicator_size, indicator_size)
        pygame.draw.rect(self.screen, color, rect)
        pygame.draw.rect(self.screen, (255, 255, 255), rect, 2)  # Border

        # Label
        text = self.small_font.render(f"P{current_player_id}", True, (255, 255, 255))
        text_rect = text.get_rect(center=rect.center)
        self.screen.blit(text, text_rect)

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
            attack_text = (
                f"Attack: {attack.attack_damage} (Range: {attack.attack_range})"
            )
            text = self.font.render(attack_text, True, (255, 255, 255))
            self.screen.blit(text, (panel_x_offset, panel_y))

        self._draw_aggregate_detection_range(game_state, [entity_id])
        self._draw_aggregate_attack_range(game_state, [entity_id])
        self._draw_unit_health_text(game_state, entity_id)

    def _draw_aggregate_detection_range(
        self, game_state: GameState, entity_ids: list[int]
    ) -> None:
        """Draws a combined detection range for multiple units."""
        detection_tiles = set()
        for entity_id in entity_ids:
            position = game_state.get_component(entity_id, Position)
            detection = game_state.get_component(entity_id, Detection)
            if not position or not detection or detection.detection_range <= 0:
                continue
            unit_x, unit_y = int(position.x), int(position.y)
            for x in range(
                unit_x - detection.detection_range,
                unit_x + detection.detection_range + 1,
            ):
                for y in range(
                    unit_y - detection.detection_range,
                    unit_y + detection.detection_range + 1,
                ):
                    if (x - unit_x) ** 2 + (
                        y - unit_y
                    ) ** 2 <= detection.detection_range**2:
                        detection_tiles.add((x, y))

        for x, y in detection_tiles:
            cam_x = (x - self.camera.x) * config.GRID_SIZE * self.camera.zoom
            cam_y = (y - self.camera.y) * config.GRID_SIZE * self.camera.zoom
            surface = pygame.Surface(
                (
                    config.GRID_SIZE * self.camera.zoom,
                    config.GRID_SIZE * self.camera.zoom,
                ),
                pygame.SRCALPHA,
            )
            pygame.draw.rect(surface, (0, 0, 255, 30), surface.get_rect())
            self.screen.blit(surface, (cam_x, cam_y))

    def _draw_aggregate_attack_range(
        self, game_state: GameState, entity_ids: list[int]
    ) -> None:
        """Draws a combined attack range for multiple units."""
        attack_tiles = set()
        for entity_id in entity_ids:
            position = game_state.get_component(entity_id, Position)
            attack = game_state.get_component(entity_id, Attack)
            if not position or not attack or attack.attack_range <= 0:
                continue
            unit_x, unit_y = int(position.x), int(position.y)
            for x in range(
                unit_x - attack.attack_range, unit_x + attack.attack_range + 1
            ):
                for y in range(
                    unit_y - attack.attack_range, unit_y + attack.attack_range + 1
                ):
                    if (x - unit_x) ** 2 + (y - unit_y) ** 2 <= attack.attack_range**2:
                        attack_tiles.add((x, y))

        for x, y in attack_tiles:
            cam_x = (x - self.camera.x) * config.GRID_SIZE * self.camera.zoom
            cam_y = (y - self.camera.y) * config.GRID_SIZE * self.camera.zoom
            surface = pygame.Surface(
                (
                    config.GRID_SIZE * self.camera.zoom,
                    config.GRID_SIZE * self.camera.zoom,
                ),
                pygame.SRCALPHA,
            )
            pygame.draw.rect(surface, (255, 0, 0, 30), surface.get_rect())
            self.screen.blit(surface, (cam_x, cam_y))

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
                int(position.x) - self.camera.x
            ) * config.GRID_SIZE * self.camera.zoom + grid_size / 2
            center_y = (
                int(position.y) - self.camera.y
            ) * config.GRID_SIZE * self.camera.zoom - 5 * self.camera.zoom
            text_rect = text.get_rect(center=(center_x, center_y))
            self.screen.blit(text, text_rect)

    def _draw_multi_unit_info(
        self, game_state: GameState, entity_ids: list[int]
    ) -> None:
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

    def _draw_active_cheats(self, cheats: dict) -> None:
        """Draws a list of active cheats."""
        active_cheats = [k.replace("_", " ").title() for k, v in cheats.items() if v]
        if not active_cheats:
            return

        y_offset = 10
        x_offset = config.SCREEN_WIDTH - 200

        title = self.font.render("Active Cheats:", True, (255, 255, 0))
        self.screen.blit(title, (x_offset, y_offset))
        y_offset += 25

        for cheat in active_cheats:
            text = self.small_font.render(cheat, True, (255, 255, 0))
            self.screen.blit(text, (x_offset + 10, y_offset))
            y_offset += 20

    def _draw_paused_message(self) -> None:
        # Dim the background
        self.screen.blit(self.pause_overlay, (0, 0))

        # Draw "Paused" text
        font = pygame.font.Font(None, 74)
        text = font.render("Paused", True, (255, 255, 255))
        text_rect = text.get_rect(
            center=(config.SCREEN_WIDTH / 2, config.SCREEN_HEIGHT / 2)
        )
        self.screen.blit(text, text_rect)

        # Draw instruction text
        small_font = pygame.font.Font(None, 36)
        instruction = small_font.render("Press P to Resume", True, (200, 200, 200))
        instruction_rect = instruction.get_rect(
            center=(config.SCREEN_WIDTH / 2, config.SCREEN_HEIGHT / 2 + 50)
        )
        self.screen.blit(instruction, instruction_rect)
