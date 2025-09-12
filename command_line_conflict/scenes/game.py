import pygame

from command_line_conflict import config
from command_line_conflict import factories
from command_line_conflict.camera import Camera
from command_line_conflict.fog_of_war import FogOfWar
from command_line_conflict.game_state import GameState
from command_line_conflict.logger import log
from command_line_conflict.maps import SimpleMap
from command_line_conflict.systems.combat_system import CombatSystem
from command_line_conflict.systems.flee_system import FleeSystem
from command_line_conflict.systems.health_system import HealthSystem
from command_line_conflict.systems.movement_system import MovementSystem
from command_line_conflict.systems.rendering_system import RenderingSystem
from command_line_conflict.systems.selection_system import SelectionSystem
from command_line_conflict.components.selectable import Selectable
from command_line_conflict.components.position import Position
from command_line_conflict.components.vision import Vision


class GameScene:
    def __init__(self, game):
        self.game = game
        self.font = game.font
        self.game_state = GameState(SimpleMap())
        self.selection_start = None
        self.camera = Camera(config.SCREEN["width"], config.SCREEN["height"])
        self.fog_of_war = FogOfWar(self.game_state.map.width, self.game_state.map.height)

        # Initialize systems
        self.movement_system = MovementSystem()
        self.rendering_system = RenderingSystem(self.game.screen, self.font, self.camera)
        self.combat_system = CombatSystem()
        self.flee_system = FleeSystem()
        self.health_system = HealthSystem()
        self.selection_system = SelectionSystem(self.camera)

    def handle_event(self, event):
        self.camera.handle_event(event)
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
            world_x, world_y = self.camera.screen_to_world(*event.pos)
            grid_x = world_x // config.GRID_SIZE
            grid_y = world_y // config.GRID_SIZE
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
            mx, my = self.camera.screen_to_world(*pygame.mouse.get_pos())
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
        self.camera.update()
        units_for_fog_of_war = []
        for _id, components in self.game_state.entities.items():
            if components.get(Position) and components.get(Vision):
                unit = type("Unit", (), {})()
                unit.x = components.get(Position).x
                unit.y = components.get(Position).y
                unit.vision_range = components.get(Vision).radius
                units_for_fog_of_war.append(unit)
        self.fog_of_war.update(units_for_fog_of_war)
        self.health_system.update(self.game_state, dt)
        self.flee_system.update(self.game_state, dt)
        self.combat_system.update(self.game_state, dt)
        self.movement_system.update(self.game_state, dt)

    def draw(self, screen):
        screen.fill((0, 0, 0))

        for x in range(0, config.SCREEN["width"], config.GRID_SIZE):
            pygame.draw.line(screen, (40, 40, 40), (x, 0), (x, config.SCREEN["height"]))
        for x in range(
            round(self.camera.x % (config.GRID_SIZE * self.camera.zoom)),
            config.SCREEN["width"],
            round(config.GRID_SIZE * self.camera.zoom),
        ):
            pygame.draw.line(
                screen, (40, 40, 40), (x, 0), (x, config.SCREEN["height"])
            )
        for y in range(
            round(self.camera.y % (config.GRID_SIZE * self.camera.zoom)),
            config.SCREEN["height"],
            round(config.GRID_SIZE * self.camera.zoom),
        ):
            pygame.draw.line(
                screen, (40, 40, 40), (0, y), (config.SCREEN["width"], y)
            )

        self.game_state.map.draw(screen, self.font, self.camera)
        self.rendering_system.draw(self.game_state)
        self.fog_of_war.draw(screen, self.camera)

        # Highlight selected units
        if self.selection_start:
            x1, y1 = self.selection_start
            x2, y2 = pygame.mouse.get_pos()
            rect = pygame.Rect(
                min(x1, x2), min(y1, y2), abs(x1 - x2), abs(y1 - y2)
            )
            overlay = pygame.Surface(rect.size, pygame.SRCALPHA)
            overlay.fill((0, 255, 0, 60))
            screen.blit(overlay, rect.topleft)
            pygame.draw.rect(screen, (0, 255, 0), rect, 1)
