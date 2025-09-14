import pygame

from command_line_conflict import config
from command_line_conflict import factories
from command_line_conflict.game_state import GameState
from command_line_conflict.logger import log
from command_line_conflict.maps import SimpleMap
from command_line_conflict.systems.combat_system import CombatSystem
from command_line_conflict.systems.flee_system import FleeSystem
from command_line_conflict.systems.health_system import HealthSystem
from command_line_conflict.systems.movement_system import MovementSystem
from command_line_conflict.systems.rendering_system import RenderingSystem
from command_line_conflict.systems.production_system import ProductionSystem
from command_line_conflict.camera import Camera
from command_line_conflict.systems.selection_system import SelectionSystem
from command_line_conflict.systems.ui_system import UISystem
from command_line_conflict.systems.corpse_removal_system import CorpseRemovalSystem
from command_line_conflict.components.selectable import Selectable
from command_line_conflict.components.position import Position
from command_line_conflict.components.renderable import Renderable
from command_line_conflict.components.production import Production


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

        # Initialize systems
        self.movement_system = MovementSystem()
        self.rendering_system = RenderingSystem(self.game.screen, self.font, self.camera)
        self.combat_system = CombatSystem()
        self.flee_system = FleeSystem()
        self.health_system = HealthSystem()
        self.selection_system = SelectionSystem()
        self.ui_system = UISystem(self.game.screen, self.font, self.camera)
        self.corpse_removal_system = CorpseRemovalSystem()
        self.production_system = ProductionSystem(self.game_state)
        self._create_initial_units()

    def _create_initial_units(self):
        """Creates the starting units for each player."""
        # Player 1 units
        for i in range(3):
            factories.create_chassis(self.game_state, 10 + i * 2, 10, player_id=1)
        # Player 2 units
        for i in range(3):
            factories.create_chassis(self.game_state, 40 + i * 2, 40, player_id=2)

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
                grid_start = self.camera.screen_to_grid(self.selection_start[0], self.selection_start[1])
                grid_end = self.camera.screen_to_grid(event.pos[0], event.pos[1])
                self.selection_system.update(
                    self.game_state, grid_start, grid_end
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
        elif event.type == pygame.KEYDOWN:
            mx, my = pygame.mouse.get_pos()
            gx, gy = self.camera.screen_to_grid(mx, my)
            if event.key == pygame.K_1:
                selected_factory = self._get_selected_factory()
                if selected_factory:
                    production = self.game_state.get_component(
                        selected_factory, Production
                    )
                    if production:
                        production.production_queue.append("chassis")
                else:
                    factories.create_extractor(self.game_state, gx, gy, player_id=1)
            elif event.key == pygame.K_2:
                selected_factory = self._get_selected_factory()
                if selected_factory:
                    production = self.game_state.get_component(
                        selected_factory, Production
                    )
                    if production:
                        production.production_queue.append("rover")
                else:
                    factories.create_chassis(self.game_state, gx, gy, player_id=1)
            elif event.key == pygame.K_3:
                factories.create_rover(self.game_state, gx, gy, player_id=1)
            elif event.key == pygame.K_4:
                factories.create_arachnotron(self.game_state, gx, gy, player_id=1)
            elif event.key == pygame.K_5:
                factories.create_observer(self.game_state, gx, gy, player_id=1)
            elif event.key == pygame.K_6:
                factories.create_immortal(self.game_state, gx, gy, player_id=1)
            elif event.key == pygame.K_b:
                for entity_id, components in self.game_state.entities.items():
                    selectable = components.get(Selectable)
                    if selectable and selectable.is_selected:
                        renderable = components.get(Renderable)
                        if renderable and renderable.icon == "E":
                            position = components.get(Position)
                            if position:
                                factories.create_factory(
                                    self.game_state,
                                    position.x + 1,
                                    position.y,
                                    player_id=1,
                                )
            elif event.key == pygame.K_w:
                self.game_state.map.add_wall(gx, gy)
            elif event.key == pygame.K_p:
                self.paused = not self.paused
            elif event.key == pygame.K_ESCAPE:
                self.game.scene_manager.switch_to("menu")
            # Camera movement (arrow keys or WASD)
            elif event.key in (pygame.K_LEFT, pygame.K_a):
                self.camera.move(-1, 0)
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                self.camera.move(1, 0)
            elif event.key in (pygame.K_UP, pygame.K_w):
                self.camera.move(0, -1)
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.camera.move(0, 1)
        # Camera zoom (mouse wheel)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Scroll up
                self.camera.zoom_in(0.1)
            elif event.button == 5:  # Scroll down
                self.camera.zoom_out(0.1)

    def _get_selected_factory(self) -> int | None:
        for entity_id, components in self.game_state.entities.items():
            selectable = components.get(Selectable)
            if selectable and selectable.is_selected:
                renderable = components.get(Renderable)
                if renderable and renderable.icon == "F":
                    return entity_id
        return None

    def update(self, dt):
        """Updates the state of all game systems.

        Args:
            dt: The time elapsed since the last frame.
        """
        if self.paused:
            return
        self.health_system.update(self.game_state, dt)
        self.flee_system.update(self.game_state, dt)
        self.combat_system.update(self.game_state, dt)
        self.movement_system.update(self.game_state, dt)
        self.corpse_removal_system.update(self.game_state, dt)
        self.production_system.update(dt)

    def draw(self, screen):
        """Draws the entire game scene.

        This includes the background grid, the map, all entities, and the UI.

        Args:
            screen: The pygame screen surface to draw on.
        """
        screen.fill((0, 0, 0))

        # Draw grid lines with camera and zoom
        grid_size = int(config.GRID_SIZE * self.camera.zoom)
        width = config.SCREEN["width"]
        height = config.SCREEN["height"]
        # Offset for camera
        cam_x = self.camera.x
        cam_y = self.camera.y
        for x in range(0, width, grid_size):
            pygame.draw.line(screen, (40, 40, 40), (x, 0), (x, height))
        for y in range(0, height, grid_size):
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
