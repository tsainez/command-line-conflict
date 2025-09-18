import pygame

from .. import config
from ..camera import Camera
from ..components.dead import Dead
from ..components.movable import Movable
from ..components.player import Player
from ..components.position import Position
from ..components.renderable import Renderable
from ..components.selectable import Selectable
from ..game_state import GameState

# TODO: Integrate logger for debug mode. Currently not used.



class RenderingSystem:
    """Handles rendering all entities and UI elements to the screen."""

    def __init__(self, screen, font, camera: Camera):
        """Initializes the RenderingSystem.
        Args:
            screen: The pygame screen surface to draw on.
            font: The pygame font to use for rendering text.
            camera: The camera object controlling view and zoom.
        """
        self.screen = screen
        self.font = font
        self.camera = camera

    def draw(self, game_state: GameState, paused: bool) -> None:
        """Draws all renderable entities to the screen.
        This method iterates through all entities, drawing them based on their
        position and state (e.g., selected, dead). It also calls other
        methods to draw additional UI elements like movement orders.
        Args:
            game_state: The current state of the game.
        """
        for entity_id, components in game_state.entities.items():
            position = components.get(Position)
            renderable = components.get(Renderable)
            player = components.get(Player)

            if position and renderable:
                dead = components.get(Dead)
                # Camera transform
                cam_x = (
                    (int(position.x) - self.camera.x)
                    * config.GRID_SIZE
                    * self.camera.zoom
                )
                cam_y = (
                    (int(position.y) - self.camera.y)
                    * config.GRID_SIZE
                    * self.camera.zoom
                )
                grid_size = int(config.GRID_SIZE * self.camera.zoom)
                if dead:
                    color = (128, 128, 128)  # Grey for dead units
                elif paused:
                    color = (128, 128, 128)  # Grey for paused units
                else:
                    color = renderable.color
                    selectable = components.get(Selectable)
                    if selectable and selectable.is_selected:
                        color = (0, 255, 0)
                        shadow_ch = self.font.render(
                            renderable.icon, True, (128, 128, 128)
                        )
                        shadow_ch = pygame.transform.scale(
                            shadow_ch, (grid_size, grid_size)
                        )
                        self.screen.blit(
                            shadow_ch,
                            (
                                cam_x + 2,
                                cam_y + 2,
                            ),
                        )

                ch = self.font.render(renderable.icon, True, color)
                ch = pygame.transform.scale(ch, (grid_size, grid_size))
                self.screen.blit(
                    ch,
                    (
                        cam_x,
                        cam_y,
                    ),
                )

                selectable = components.get(Selectable)
                if not dead:
                    if selectable and selectable.is_selected:
                        self.draw_orders(components)
                    elif config.DEBUG:
                        self.draw_orders(components)

    def draw_orders(self, components) -> None:
        """Draws the movement path and target for a selected entity.

        Args:
            components: The component dictionary for the entity.
        """
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
            cam_x = (tx - self.camera.x) * config.GRID_SIZE * self.camera.zoom
            cam_y = (ty - self.camera.y) * config.GRID_SIZE * self.camera.zoom
            self.screen.blit(ch, (cam_x, cam_y))
            prev_x, prev_y = tx, ty

        tx, ty = tiles[-1]
        final_char = "X"
        ch = self.font.render(final_char, True, (255, 0, 0))
        cam_x = (tx - self.camera.x) * config.GRID_SIZE * self.camera.zoom
        cam_y = (ty - self.camera.y) * config.GRID_SIZE * self.camera.zoom
        self.screen.blit(ch, (cam_x, cam_y))

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
