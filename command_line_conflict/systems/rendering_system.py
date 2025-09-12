import pygame
from ..game_state import GameState
from ..components.position import Position
from ..components.renderable import Renderable
from ..components.selectable import Selectable
from ..components.movable import Movable
from ..components.dead import Dead
from .. import config


class RenderingSystem:
    """
    This system is responsible for rendering entities on the screen.
    """

    def __init__(self, screen, font):
        self.screen = screen
        self.font = font

    def draw(self, game_state: GameState) -> None:
        for entity_id, components in game_state.entities.items():
            position = components.get(Position)
            renderable = components.get(Renderable)

            if position and renderable:
                dead = components.get(Dead)
                if dead:
                    color = (128, 128, 128)  # Grey for dead units
                else:
                    color = (255, 255, 255)
                    selectable = components.get(Selectable)
                    if selectable and selectable.is_selected:
                        color = (0, 255, 0)
                        shadow_ch = self.font.render(
                            renderable.icon, True, (128, 128, 128)
                        )
                        self.screen.blit(
                            shadow_ch,
                            (
                                int(position.x) * config.GRID_SIZE + 2,
                                int(position.y) * config.GRID_SIZE + 2,
                            ),
                        )

                ch = self.font.render(renderable.icon, True, color)
                self.screen.blit(
                    ch,
                    (
                        int(position.x) * config.GRID_SIZE,
                        int(position.y) * config.GRID_SIZE,
                    ),
                )

                selectable = components.get(Selectable)
                if not dead and selectable and selectable.is_selected:
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

        prev_x, prev_y = int(position.x), int(position.y)
        for tx, ty in tiles[:-1]:
            arrow = self._arrow_char(tx - prev_x, ty - prev_y)
            ch = self.font.render(arrow, True, (0, 255, 0))
            self.screen.blit(ch, (tx * config.GRID_SIZE, ty * config.GRID_SIZE))
            prev_x, prev_y = tx, ty

        tx, ty = tiles[-1]
        final_char = "X"
        ch = self.font.render(final_char, True, (255, 0, 0))
        self.screen.blit(ch, (tx * config.GRID_SIZE, ty * config.GRID_SIZE))

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
