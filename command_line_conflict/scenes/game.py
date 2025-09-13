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
from command_line_conflict.systems.selection_system import SelectionSystem
from command_line_conflict.systems.ui_system import UISystem
from command_line_conflict.systems.corpse_removal_system import CorpseRemovalSystem
from command_line_conflict.components.selectable import Selectable


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

        # Initialize systems
        self.movement_system = MovementSystem()
        self.rendering_system = RenderingSystem(self.game.screen, self.font)
        self.combat_system = CombatSystem()
        self.flee_system = FleeSystem()
        self.health_system = HealthSystem()
        self.selection_system = SelectionSystem()
        self.ui_system = UISystem(self.game.screen, self.font)
        self.corpse_removal_system = CorpseRemovalSystem()

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
                log.debug(f"Click selection at {event.pos}. Shift: {shift_pressed}")
                self.selection_system.handle_click_selection(
                    self.game_state, event.pos, shift_pressed
                )
            else:
                log.debug(f"Drag selection from {self.selection_start} to {event.pos}")
                self.selection_system.update(
                    self.game_state, self.selection_start, event.pos
                )
            self.selection_start = None
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            grid_x = event.pos[0] // config.GRID_SIZE
            grid_y = event.pos[1] // config.GRID_SIZE
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
            gx = mx // config.GRID_SIZE
            gy = my // config.GRID_SIZE
            if event.key == pygame.K_1:
                factories.create_extractor(self.game_state, gx, gy)
            elif event.key == pygame.K_2:
                factories.create_chassis(self.game_state, gx, gy)
            elif event.key == pygame.K_3:
                factories.create_rover(self.game_state, gx, gy)
            elif event.key == pygame.K_4:
                factories.create_arachnotron(self.game_state, gx, gy)
            elif event.key == pygame.K_5:
                factories.create_observer(self.game_state, gx, gy)
            elif event.key == pygame.K_6:
                factories.create_immortal(self.game_state, gx, gy)
            elif event.key == pygame.K_w:
                self.game_state.map.add_wall(gx, gy)
            elif event.key == pygame.K_q:
                self.game.running = False
            elif event.key == pygame.K_ESCAPE:
                self.game.scene_manager.switch_to("menu")

    def update(self, dt):
        """Updates the state of all game systems.

        Args:
            dt: The time elapsed since the last frame.
        """
        self.health_system.update(self.game_state, dt)
        self.flee_system.update(self.game_state, dt)
        self.combat_system.update(self.game_state, dt)
        self.movement_system.update(self.game_state, dt)
        self.corpse_removal_system.update(self.game_state, dt)

    def draw(self, screen):
        """Draws the entire game scene.

        This includes the background grid, the map, all entities, and the UI.

        Args:
            screen: The pygame screen surface to draw on.
        """
        screen.fill((0, 0, 0))

        for x in range(0, config.SCREEN["width"], config.GRID_SIZE):
            pygame.draw.line(screen, (40, 40, 40), (x, 0), (x, config.SCREEN["height"]))
        for y in range(0, config.SCREEN["height"], config.GRID_SIZE):
            pygame.draw.line(screen, (40, 40, 40), (0, y), (config.SCREEN["width"], y))

        self.game_state.map.draw(screen, self.font)
        self.rendering_system.draw(self.game_state)
        self.ui_system.draw(self.game_state)

        # Highlight selected units
        if self.selection_start:
            x1, y1 = self.selection_start
            x2, y2 = pygame.mouse.get_pos()
            min_x, max_x = sorted((x1, x2))
            min_y, max_y = sorted((y1, y2))
            min_x = (min_x // config.GRID_SIZE) * config.GRID_SIZE
            min_y = (min_y // config.GRID_SIZE) * config.GRID_SIZE
            max_x = ((max_x // config.GRID_SIZE) + 1) * config.GRID_SIZE
            max_y = ((max_y // config.GRID_SIZE) + 1) * config.GRID_SIZE
            rect = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)
            overlay = pygame.Surface(rect.size, pygame.SRCALPHA)
            overlay.fill((0, 255, 0, 60))
            screen.blit(overlay, rect.topleft)
            pygame.draw.rect(screen, (0, 255, 0), rect, 1)
