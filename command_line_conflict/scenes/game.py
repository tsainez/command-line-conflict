import math

import pygame

from command_line_conflict import config, factories
from command_line_conflict.camera import Camera
from command_line_conflict.components.attack import Attack
from command_line_conflict.components.selectable import Selectable
from command_line_conflict.game_state import GameState
from command_line_conflict.logger import log
from command_line_conflict.maps import SimpleMap
from command_line_conflict.systems.ai_system import AISystem
from command_line_conflict.systems.combat_system import CombatSystem
from command_line_conflict.systems.confetti_system import ConfettiSystem
from command_line_conflict.systems.corpse_removal_system import CorpseRemovalSystem
from command_line_conflict.systems.flee_system import FleeSystem
from command_line_conflict.systems.health_system import HealthSystem
from command_line_conflict.systems.movement_system import MovementSystem
from command_line_conflict.systems.rendering_system import RenderingSystem
from command_line_conflict.systems.selection_system import SelectionSystem
from command_line_conflict.systems.sound_system import SoundSystem
from command_line_conflict.systems.spawn_system import SpawnSystem
from command_line_conflict.systems.ui_system import UISystem
from command_line_conflict.systems.wander_system import WanderSystem


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
        self.sound_system = SoundSystem()
        self.wander_system = WanderSystem()
        self.spawn_system = SpawnSystem(spawn_interval=5.0)  # Spawn every 5 seconds
        self._create_initial_units()

        # Start game music
        # Assuming the music file is in the root or a music folder
        # For now using a placeholder path
        self.game.music_manager.play("music/game_theme.ogg")

    def _create_initial_units(self):
        """Creates the starting units for each player."""
        # Player 1 units (human)
        for i in range(3):
            factories.create_chassis(
                self.game_state, 10 + i * 2, 10, player_id=1, is_human=True
            )
        # Player 2 units (AI)
        for i in range(3):
            factories.create_chassis(
                self.game_state, 40 + i * 2, 40, player_id=2, is_human=False
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
                    # Moving clears hold position
                    from command_line_conflict.components.movable import Movable

                    movable = components.get(Movable)
                    if movable:
                        movable.hold_position = False

                    self.movement_system.set_target(
                        self.game_state, entity_id, grid_x, grid_y
                    )
                    attack = components.get(Attack)
                    if attack:
                        attack.attack_target = None
        elif event.type == pygame.KEYDOWN:
            # Camera movement
            if event.key in (pygame.K_UP, pygame.K_w):
                self.camera_movement["up"] = True
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.camera_movement["down"] = True
            elif event.key in (pygame.K_LEFT, pygame.K_a):
                self.camera_movement["left"] = True
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                self.camera_movement["right"] = True
            else:
                mx, my = pygame.mouse.get_pos()
                gx, gy = self.camera.screen_to_grid(mx, my)
                if event.key == pygame.K_1:
                    factories.create_extractor(
                        self.game_state, gx, gy, player_id=1, is_human=True
                    )
                elif event.key == pygame.K_2:
                    factories.create_chassis(
                        self.game_state, gx, gy, player_id=1, is_human=True
                    )
                elif event.key == pygame.K_3:
                    factories.create_rover(
                        self.game_state, gx, gy, player_id=1, is_human=True
                    )
                elif event.key == pygame.K_4:
                    factories.create_arachnotron(
                        self.game_state, gx, gy, player_id=1, is_human=True
                    )
                elif event.key == pygame.K_5:
                    factories.create_observer(
                        self.game_state, gx, gy, player_id=1, is_human=True
                    )
                elif event.key == pygame.K_6:
                    factories.create_immortal(
                        self.game_state, gx, gy, player_id=1, is_human=True
                    )
                elif event.key == pygame.K_h:
                    # Hold Position
                    from command_line_conflict.components.movable import Movable

                    for entity_id, components in self.game_state.entities.items():
                        selectable = components.get(Selectable)
                        if selectable and selectable.is_selected:
                            movable = components.get(Movable)
                            if movable:
                                movable.hold_position = True
                                movable.path = []
                                movable.target_x = None
                                movable.target_y = None
                                log.info(f"Entity {entity_id} holding position")

                elif event.key == pygame.K_p:
                    self.paused = not self.paused
                elif event.key == pygame.K_ESCAPE:
                    self.game.scene_manager.switch_to("menu")
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

    def update(self, dt):
        """Updates the state of all game systems.

        Args:
            dt: The time elapsed since the last frame.
        """
        if self.paused:
            return
        self._update_camera(dt)
        self.health_system.update(self.game_state, dt)
        self.flee_system.update(self.game_state, dt)
        self.ai_system.update(self.game_state)
        self.wander_system.update(self.game_state, dt)
        self.combat_system.update(self.game_state, dt)
        self.confetti_system.update(self.game_state, dt)
        self.movement_system.update(self.game_state, dt)
        self.corpse_removal_system.update(self.game_state, dt)
        self.sound_system.update(self.game_state)

        # Clear event queue after all systems have processed events
        self.game_state.event_queue.clear()
        self.spawn_system.update(self.game_state, dt)

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
        self.ui_system.draw(self.game_state, self.paused)

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
