import os
from pathlib import Path

import pygame

from . import config
from .maps import Map, SimpleMap
from .units import Airplane
from .units import base as unit_base


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
                unit_base.USE_ASCII = False
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
                unit_base.USE_ASCII = False
            else:
                # Final fallback to generic monospace and ASCII graphics
                self.font = pygame.font.SysFont("monospace", 16)
                unit_base.USE_ASCII = True

        self.map = game_map or SimpleMap()
        self.selection_start = None
        self.running = True

    def handle_event(self, event) -> None:
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.selection_start = event.pos
            for u in self.map.units:
                u.selected = False
        elif (
            event.type == pygame.MOUSEBUTTONUP
            and event.button == 1
            and self.selection_start
        ):
            x1, y1 = self.selection_start
            x2, y2 = event.pos
            self.selection_start = None

            sx, ex = sorted((x1 // config.GRID_SIZE, x2 // config.GRID_SIZE))
            sy, ey = sorted((y1 // config.GRID_SIZE, y2 // config.GRID_SIZE))

            for u in self.map.units:
                ux = int(u.x)
                uy = int(u.y)
                if sx <= ux <= ex and sy <= uy <= ey:
                    u.selected = True
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            grid_x = event.pos[0] // config.GRID_SIZE
            grid_y = event.pos[1] // config.GRID_SIZE
            for u in self.map.units:
                if u.selected:
                    u.set_target(grid_x, grid_y, self.map)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_a:
            mx, my = pygame.mouse.get_pos()
            gx = mx // config.GRID_SIZE
            gy = my // config.GRID_SIZE
            self.map.spawn_unit(Airplane(gx, gy))

    def update(self, dt: float) -> None:
        self.map.update(dt)

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

        self.map.draw(self.screen, self.font)
        for u in self.map.units:
            u.draw(self.screen, self.font)

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
