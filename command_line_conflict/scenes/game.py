import math

import pygame

from command_line_conflict import config, factories
from command_line_conflict.camera import Camera
from command_line_conflict.components.attack import Attack
from command_line_conflict.components.builder import Builder
from command_line_conflict.components.building import Building
from command_line_conflict.components.factory import Factory
from command_line_conflict.components.player import Player
from command_line_conflict.components.position import Position
from command_line_conflict.components.renderable import Renderable
from command_line_conflict.components.selectable import Selectable
from command_line_conflict.game_state import GameState
from command_line_conflict.logger import log
from command_line_conflict.maps import SimpleMap
from command_line_conflict.systems.ai_system import AISystem
from command_line_conflict.systems.build_system import BuildSystem
from command_line_conflict.systems.combat_system import CombatSystem
from command_line_conflict.systems.confetti_system import ConfettiSystem
from command_line_conflict.systems.corpse_removal_system import \
    CorpseRemovalSystem
from command_line_conflict.systems.factory_system import FactorySystem
from command_line_conflict.systems.flee_system import FleeSystem
from command_line_conflict.systems.health_system import HealthSystem
from command_line_conflict.systems.movement_system import MovementSystem
from command_line_conflict.systems.rendering_system import RenderingSystem
from command_line_conflict.systems.selection_system import SelectionSystem
from command_line_conflict.systems.ui_system import UISystem


class GameScene:
    """Manages the main gameplay scene, including entities, systems, and events."""

    def __init__(self, game):
        """Initializes the GameScene.

        Args:
            game: The main game object, providing access to the screen, font,
                  and scene manager.
        """
        self.game = game
        self.font = game.font
        self.game_state = GameState(SimpleMap())
        self.selection_start = None
        self.paused = False
        self.game_over = False
        self.winner = None
        self.player1_has_buildings = False
        self.player2_has_buildings = False

        # Camera
        self.camera = Camera()
        self.camera_movement = {
            "up": False,
            "down": False,
            "left": False,
            "right": False,
        }

        # Initialize systems
        self.movement_system = MovementSystem()
        self.rendering_system = RenderingSystem(
            self.game.screen, self.font, self.camera
        )
        self.combat_system = CombatSystem()
        self.flee_system = FleeSystem()
        self.health_system = HealthSystem()
        self.selection_system = SelectionSystem()
        self.ui_system = UISystem(self.game.screen, self.font, self.camera)
        self.corpse_removal_system = CorpseRemovalSystem()
        self.ai_system = AISystem()
        self.confetti_system = ConfettiSystem()
        self.build_system = BuildSystem()
        self.factory_system = FactorySystem()
        self._create_initial_units()

    def _create_initial_units(self):
        """Creates the starting units and mineral patches for each player."""
        # Player 1 (human)
        factories.create_minerals(self.game_state, 10, 10)
        for i in range(3):
            factories.create_extractor(
                self.game_state, 8, 8 + i * 2, player_id=1, is_human=True
            )

        # Player 2 (AI)
        factories.create_minerals(self.game_state, 40, 40)
        for i in range(3):
            factories.create_extractor(
                self.game_state, 42, 38 + i * 2, player_id=2, is_human=False
            )

    def handle_event(self, event):
        """Handles user input and other events for the game scene.

        This includes mouse clicks for selection and movement, as well as
        keyboard shortcuts for creating units and quitting the game.

        Args:
            event: The pygame event to handle.
        """
        log.debug(f"Handling event: {event}")
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.selection_start = event.pos
        elif (
            event.type == pygame.MOUSEBUTTONUP
            and event.button == 1
            and self.selection_start
        ):
            x1, y1 = self.selection_start
            x2, y2 = event.pos
            # If the mouse moved less than 5 pixels, it's a click
            if (x2 - x1) ** 2 + (y2 - y1) ** 2 < 25:
                mods = pygame.key.get_mods()
                shift_pressed = mods & pygame.KMOD_SHIFT
                grid_pos = self.camera.screen_to_grid(event.pos[0], event.pos[1])
                log.debug(f"Click selection at {grid_pos}. Shift: {shift_pressed}")
                self.selection_system.handle_click_selection(
                    self.game_state, grid_pos, shift_pressed
                )
            else:
                log.debug(f"Drag selection from {self.selection_start} to {event.pos}")
                mods = pygame.key.get_mods()
                shift_pressed = mods & pygame.KMOD_SHIFT
                grid_start = self.camera.screen_to_grid(
                    self.selection_start[0], self.selection_start[1]
                )
                grid_end = self.camera.screen_to_grid(event.pos[0], event.pos[1])
                self.selection_system.update(
                    self.game_state, grid_start, grid_end, shift_pressed
                )
            self.selection_start = None
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            grid_x, grid_y = self.camera.screen_to_grid(event.pos[0], event.pos[1])
            log.debug(
                f"Right-click move command at grid coordinates: {(grid_x, grid_y)}"
            )
            for entity_id, components in self.game_state.entities.items():
                selectable = components.get(Selectable)
                if selectable and selectable.is_selected:
                    log.info(f"Moving entity {entity_id} to {(grid_x, grid_y)}")
                    self.movement_system.set_target(
                        self.game_state, entity_id, grid_x, grid_y
                    )
                    attack = components.get(Attack)
                    if attack:
                        attack.attack_target = None
        elif event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                self.camera_movement["up"] = True
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.camera_movement["down"] = True
            elif event.key in (pygame.K_LEFT, pygame.K_a):
                self.camera_movement["left"] = True
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                self.camera_movement["right"] = True
            elif event.key == pygame.K_p:
                self.paused = not self.paused
            elif event.key == pygame.K_ESCAPE:
                self.game.scene_manager.switch_to("menu")
            else:
                self.handle_action_keys(event.key)
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_UP, pygame.K_w):
                self.camera_movement["up"] = False
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.camera_movement["down"] = False
            elif event.key in (pygame.K_LEFT, pygame.K_a):
                self.camera_movement["left"] = False
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                self.camera_movement["right"] = False
        # Camera zoom (mouse wheel)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Scroll up
                self.camera.zoom_in(0.1)
            elif event.button == 5:  # Scroll down
                self.camera.zoom_out(0.1)

    def handle_action_keys(self, key):
        """Handles keyboard shortcuts for in-game actions."""
        selected_units = []
        for entity_id, components in self.game_state.entities.items():
            selectable = components.get(Selectable)
            if selectable and selectable.is_selected:
                selected_units.append((entity_id, components))

        if not selected_units:
            return

        # For now, commands apply to the first selected unit
        entity_id, components = selected_units[0]
        player = components.get(Player)
        if not player or not player.is_human:
            return

        # Builder actions
        builder = components.get(Builder)
        if builder and key == pygame.K_f and "unit_factory" in builder.build_types:
            cost = config.UNIT_COSTS["unit_factory"]
            if self.game_state.resources[player.player_id]["minerals"] >= cost["minerals"]:
                mx, my = pygame.mouse.get_pos()
                gx, gy = self.camera.screen_to_grid(mx, my)
                self.game_state.resources[player.player_id]["minerals"] -= cost["minerals"]
                site_id = self.game_state.create_entity()
                self.game_state.add_component(site_id, Position(gx, gy))
                self.game_state.add_component(site_id, Renderable(icon="X", color=(128, 128, 128)))
                self.game_state.add_component(site_id, Building())
                self.game_state.add_component(site_id, Player(player.player_id, player.is_human))
                builder.build_target = site_id
                self.movement_system.set_target(self.game_state, entity_id, gx, gy)
                log.info(f"Player {player.player_id} building a factory at {(gx, gy)}.")
                if player.player_id == 1:
                    self.player1_has_buildings = True
                else:
                    self.player2_has_buildings = True

        # Factory actions
        factory = components.get(Factory)
        if factory:
            unit_to_build = None
            if key == pygame.K_c and "chassis" in factory.unit_types:
                unit_to_build = "chassis"
            elif key == pygame.K_e and "extractor" in factory.unit_types:
                unit_to_build = "extractor"

            if unit_to_build:
                cost = config.UNIT_COSTS[unit_to_build]
                if self.game_state.resources[player.player_id]["minerals"] >= cost["minerals"]:
                    self.game_state.resources[player.player_id]["minerals"] -= cost["minerals"]
                    factory.production_queue.append(unit_to_build)
                    log.info(f"Factory {entity_id} queued a {unit_to_build}.")


    def _update_camera(self, dt):
        """Updates the camera position based on user input."""
        if self.camera_movement["up"]:
            self.camera.move(0, -config.CAMERA_SPEED * dt)
        if self.camera_movement["down"]:
            self.camera.move(0, config.CAMERA_SPEED * dt)
        if self.camera_movement["left"]:
            self.camera.move(-config.CAMERA_SPEED * dt, 0)
        if self.camera_movement["right"]:
            self.camera.move(config.CAMERA_SPEED * dt, 0)

    def _check_win_condition(self):
        if self.game_over:
            return

        player1_building_count = 0
        player2_building_count = 0

        for entity_id, components in self.game_state.entities.items():
            if components.get(Building):
                player = components.get(Player)
                if player:
                    if player.player_id == 1:
                        player1_building_count += 1
                    elif player.player_id == 2:
                        player2_building_count += 1

        if self.player1_has_buildings and player1_building_count == 0:
            self.game_over = True
            self.winner = 2
            log.info("Player 2 wins!")
        elif self.player2_has_buildings and player2_building_count == 0:
            self.game_over = True
            self.winner = 1
            log.info("Player 1 wins!")

    def update(self, dt):
        """Updates the state of all game systems.

        Args:
            dt: The time elapsed since the last frame.
        """
        if self.game_over or self.paused:
            return
        self._update_camera(dt)
        self.health_system.update(self.game_state, dt)
        self.flee_system.update(self.game_state, dt)
        self.ai_system.update(self.game_state)
        self.combat_system.update(self.game_state, dt)
        self.confetti_system.update(self.game_state, dt)
        self.movement_system.update(self.game_state, dt)
        self.corpse_removal_system.update(self.game_state, dt)
        self.build_system.update(self.game_state, dt)
        self.factory_system.update(self.game_state, dt)
        self._check_win_condition()

    def draw(self, screen):
        """Draws the entire game scene.

        This includes the background grid, the map, all entities, and the UI.

        Args:
            screen: The pygame screen surface to draw on.
        """
        screen.fill((0, 0, 0))

        # Draw grid lines with camera and zoom
        grid_size = int(config.GRID_SIZE * self.camera.zoom)
        if grid_size > 0:
            width, height = self.game.screen.get_size()
            start_x = (math.floor(self.camera.x) - self.camera.x) * grid_size
            start_y = (math.floor(self.camera.y) - self.camera.y) * grid_size

            for x in range(int(start_x), width, grid_size):
                pygame.draw.line(screen, (40, 40, 40), (x, 0), (x, height))
            for y in range(int(start_y), height, grid_size):
                pygame.draw.line(screen, (40, 40, 40), (0, y), (width, y))

        self.game_state.map.draw(screen, self.font, camera=self.camera)
        self.rendering_system.draw(self.game_state, self.paused)
        self.ui_system.draw(
            self.game_state, self.paused, self.game_over, self.winner
        )

        # Highlight selected units
        if self.selection_start:
            x1, y1 = self.selection_start
            x2, y2 = pygame.mouse.get_pos()
            min_x, max_x = sorted((x1, x2))
            min_y, max_y = sorted((y1, y2))
            rect = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)
            overlay = pygame.Surface(rect.size, pygame.SRCALPHA)
            overlay.fill((0, 255, 0, 60))
            screen.blit(overlay, rect.topleft)
            pygame.draw.rect(screen, (0, 255, 0), rect, 1)