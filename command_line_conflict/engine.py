import os
from pathlib import Path

import pygame

from . import config
from . import factories
from .game_state import GameState
from .maps import Map, SimpleMap
from .systems.combat_system import CombatSystem
from .systems.flee_system import FleeSystem
from .systems.health_system import HealthSystem
from .systems.movement_system import MovementSystem
from .systems.rendering_system import RenderingSystem
from .systems.selection_system import SelectionSystem


class Game:
    """Main game engine."""

    def __init__(self, game_map: Map | None = None) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode(
            (config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
        )
        pygame.display.set_caption("ASCII RTS")
        self.clock = pygame.time.Clock()

        # Prefer the bundled DejaVu font for rendering path arrows
        font_dir = Path(__file__).resolve().parent / "fonts"
        bundled = font_dir / "DejaVuSansMono.ttf"
        self.font = None
        if bundled.exists():
            try:
                self.font = pygame.font.Font(str(bundled), 16)
            except Exception:
                self.font = None

        if self.font is None:
            # Try common system fonts
            candidates = [
                "dejavusansmono",
                "couriernew",
                "menlo",
                "consolas",
            ]
            font_path = None
            for name in candidates:
                font_path = pygame.font.match_font(name)
                if font_path:
                    break

            if font_path:
                self.font = pygame.font.Font(font_path, 16)
            else:
                # Final fallback to generic monospace and ASCII graphics
                self.font = pygame.font.SysFont("monospace", 16)

        game_map = game_map or SimpleMap()
        self.game_state = GameState(game_map)
        self.selection_start = None
        self.running = True

        # Initialize systems
        self.movement_system = MovementSystem()
        self.rendering_system = RenderingSystem(self.screen, self.font)
        self.combat_system = CombatSystem()
        self.flee_system = FleeSystem()
        self.health_system = HealthSystem()
        self.selection_system = SelectionSystem()

    def handle_event(self, event) -> None:
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
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
                self.selection_system.handle_click_selection(
                    self.game_state, event.pos, shift_pressed
                )
            else:
                self.selection_system.update(
                    self.game_state, self.selection_start, event.pos
                )
            self.selection_start = None
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            grid_x = event.pos[0] // config.GRID_SIZE
            grid_y = event.pos[1] // config.GRID_SIZE
            for entity_id, components in self.game_state.entities.items():
                selectable = components.get("Selectable")
                if selectable and selectable.is_selected:
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
                self.running = False

    def update(self, dt: float) -> None:
        self.health_system.update(self.game_state, dt)
        self.flee_system.update(self.game_state, dt)
        self.combat_system.update(self.game_state, dt)
        self.movement_system.update(self.game_state, dt)

    def draw(self) -> None:
        self.screen.fill((0, 0, 0))

        for x in range(0, config.SCREEN_WIDTH, config.GRID_SIZE):
            pygame.draw.line(
                self.screen, (40, 40, 40), (x, 0), (x, config.SCREEN_HEIGHT)
            )
        for y in range(0, config.SCREEN_HEIGHT, config.GRID_SIZE):
            pygame.draw.line(
                self.screen, (40, 40, 40), (0, y), (config.SCREEN_WIDTH, y)
            )

        self.game_state.map.draw(self.screen, self.font)
        self.rendering_system.draw(self.game_state)

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
            self.screen.blit(overlay, rect.topleft)
            pygame.draw.rect(self.screen, (0, 255, 0), rect, 1)

        pygame.display.flip()

    def run(self) -> None:
        while self.running:
            dt = self.clock.tick(config.FPS) / 1000.0
            for event in pygame.event.get():
                self.handle_event(event)
            self.update(dt)
            self.draw()
        pygame.quit()


def main(game_map: Map | None = None) -> None:
    """Helper to launch the game with a given map."""
    Game(game_map).run()


if __name__ == "__main__":
    main()
