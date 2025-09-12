import pygame
from ..game_state import GameState
from ..components.position import Position
from ..components.renderable import Renderable
from ..components.selectable import Selectable
from ..components.movable import Movable
from .. import config


from ..camera import Camera


class RenderingSystem:
    """
    This system is responsible for rendering entities on the screen.
    """

    def __init__(self, screen, font, camera: Camera):
        self.screen = screen
        self.font = font
        self.camera = camera

    def draw(self, game_state: GameState) -> None:
        for entity_id, components in game_state.entities.items():
            position = components.get(Position)
            renderable = components.get(Renderable)

            if position and renderable:
                color = (255, 255, 255)
                selectable = components.get(Selectable)
                if selectable and selectable.is_selected:
                    color = (0, 255, 0)

                # Apply camera zoom to font size
                font_size = int(config.GRID_SIZE * self.camera.zoom)
                if font_size <= 0:
                    continue
                font = pygame.font.Font(self.font.get_path(), font_size)
                ch = font.render(renderable.icon, True, color)

                screen_pos = self.camera.world_to_screen(
                    int(position.x) * config.GRID_SIZE,
                    int(position.y) * config.GRID_SIZE,
                )
                self.screen.blit(ch, screen_pos)

                if selectable and selectable.is_selected:
                    self.draw_orders(components)

    def draw_orders(self, components) -> None:
        movable = components.get(Movable)
        if not movable:
            return

        position = components.get(Position)
        if not position:
            return

        if movable.path:
            final = movable.path[-1]
        elif movable.target_x is not None and movable.target_y is not None:
            final = (int(movable.target_x), int(movable.target_y))
        else:
            final = (int(position.x), int(position.y))

        if not movable.path and final == (int(position.x), int(position.y)):
            return

        tiles = list(movable.path)
        if not tiles and movable.can_fly:
            tiles = self._direct_line((int(position.x), int(position.y)), final)
        if not tiles or tiles[-1] != final:
            tiles.append(final)

        font_size = int(config.GRID_SIZE * self.camera.zoom)
        if font_size <= 0:
            return
        font = pygame.font.Font(self.font.get_path(), font_size)

        prev_x, prev_y = int(position.x), int(position.y)
        for tx, ty in tiles[:-1]:
            arrow = self._arrow_char(tx - prev_x, ty - prev_y)
            ch = font.render(arrow, True, (0, 255, 0))
            screen_pos = self.camera.world_to_screen(
                tx * config.GRID_SIZE, ty * config.GRID_SIZE
            )
            self.screen.blit(ch, screen_pos)
            prev_x, prev_y = tx, ty

        tx, ty = tiles[-1]
        final_char = "X"
        ch = font.render(final_char, True, (255, 0, 0))
        screen_pos = self.camera.world_to_screen(
            tx * config.GRID_SIZE, ty * config.GRID_SIZE
        )
        self.screen.blit(ch, screen_pos)

    @staticmethod
    def _direct_line(
        start: tuple[int, int], end: tuple[int, int]
    ) -> list[tuple[int, int]]:
        """Return a simple diagonal path from ``start`` to ``end``."""
        x, y = start
        path: list[tuple[int, int]] = []
        while (x, y) != end:
            if x < end[0]:
                x += 1
            elif x > end[0]:
                x -= 1
            if y < end[1]:
                y += 1
            elif y > end[1]:
                y -= 1
            path.append((x, y))
        return path

    @staticmethod
    def _arrow_char(dx: int, dy: int) -> str:
        """Return a character representing movement direction."""
        dx = (dx > 0) - (dx < 0)
        dy = (dy > 0) - (dy < 0)
        if dx == 1 and dy == 0:
            return ">"
        if dx == -1 and dy == 0:
            return "<"
        if dx == 0 and dy == 1:
            return "v"
        if dx == 0 and dy == -1:
            return "^"
        if dx == 1 and dy == 1:
            return "\\"
        if dx == -1 and dy == -1:
            return "\\"
        if dx == 1 and dy == -1:
            return "/"
        if dx == -1 and dy == 1:
            return "/"
        if dx != 0:
            return "-"
        if dy != 0:
            return "|"
        return "+"
