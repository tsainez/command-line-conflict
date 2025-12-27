import functools

import pygame

from .. import config
from ..camera import Camera
from ..components.confetti import Confetti
from ..components.dead import Dead
from ..components.health import Health
from ..components.movable import Movable
from ..components.position import Position
from ..components.renderable import Renderable
from ..components.selectable import Selectable
from ..game_state import GameState
from ..logger import log


class RenderingSystem:
    """Handles rendering all entities and UI elements to the screen.

    Optimized to use spatial hashing for performance.
    """

    # Pre-defined colors for confetti to avoid allocation per frame
    CONFETTI_COLORS = [
        (255, 0, 0),
        (0, 255, 0),
        (0, 0, 255),
        (255, 255, 0),
        (255, 0, 255),
        (0, 255, 255),
    ]

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
        log.debug("RenderingSystem initialized")

    @functools.lru_cache(maxsize=1024)
    def _get_rendered_surface(self, char: str, color: tuple, size: int | None = None) -> pygame.Surface:
        """Returns a cached surface for the character, optionally scaled."""
        s = self.font.render(char, True, color)
        if size is not None:
            s = pygame.transform.scale(s, (size, size))
        return s

    def draw(self, game_state: GameState, paused: bool) -> None:
        """Draws all renderable entities to the screen.

        This method iterates through visible entities using the spatial map,
        drawing them based on their position and state.
        """
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        tile_size = config.GRID_SIZE * self.camera.zoom

        # Calculate visible grid bounds with buffer
        start_x = int(self.camera.x) - 1
        end_x = int(self.camera.x + screen_width / tile_size) + 2
        start_y = int(self.camera.y) - 1
        end_y = int(self.camera.y + screen_height / tile_size) + 2

        # Iterate through visible tiles
        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                entity_ids = game_state.spatial_map.get((x, y))
                if not entity_ids:
                    continue

                for entity_id in entity_ids:
                    components = game_state.entities.get(entity_id)
                    if not components:
                        continue

                    position = components.get(Position)
                    renderable = components.get(Renderable)

                    if not position or not renderable:
                        continue

                    # Camera transform
                    cam_x = (int(position.x) - self.camera.x) * config.GRID_SIZE * self.camera.zoom
                    cam_y = (int(position.y) - self.camera.y) * config.GRID_SIZE * self.camera.zoom
                    grid_size = int(config.GRID_SIZE * self.camera.zoom)

                    confetti = components.get(Confetti)
                    if confetti:
                        # Confetti is just a particle, so it should be simple
                        # Optimization: Use deterministic color based on ID to avoid
                        # list allocation and random.choice() per frame.
                        # Also prevents visual flickering.
                        color = self.CONFETTI_COLORS[entity_id % len(self.CONFETTI_COLORS)]
                        ch = self._get_rendered_surface(renderable.icon, color, grid_size)
                        self.screen.blit(
                            ch,
                            (
                                cam_x,
                                cam_y,
                            ),
                        )
                        continue

                    dead = components.get(Dead)
                    if dead:
                        color = (128, 128, 128)  # Grey for dead units
                    elif paused:
                        color = (128, 128, 128)  # Grey for paused units
                    else:
                        color = renderable.color
                        selectable = components.get(Selectable)
                        if selectable and selectable.is_selected:
                            color = (0, 255, 0)
                            shadow_ch = self._get_rendered_surface(renderable.icon, (128, 128, 128), grid_size)
                            self.screen.blit(
                                shadow_ch,
                                (
                                    cam_x + 2,
                                    cam_y + 2,
                                ),
                            )

                    ch = self._get_rendered_surface(renderable.icon, color, grid_size)
                    self.screen.blit(
                        ch,
                        (
                            cam_x,
                            cam_y,
                        ),
                    )

                    health = components.get(Health)
                    if not dead and health and health.max_hp > 0:
                        health_pct = max(0.0, min(1.0, health.hp / health.max_hp))
                        bar_width = grid_size
                        bar_height = max(4, int(grid_size * 0.2))
                        bar_x = cam_x
                        bar_y = cam_y - bar_height - 2

                        # Determine color based on health percentage
                        if health_pct > 0.5:
                            hp_color = (0, 255, 0)  # Green
                        elif health_pct > 0.25:
                            hp_color = (255, 255, 0)  # Yellow
                        else:
                            hp_color = (255, 0, 0)  # Red

                        # Draw background (dark grey)
                        pygame.draw.rect(
                            self.screen,
                            (60, 60, 60),
                            (bar_x, bar_y, bar_width, bar_height),
                        )
                        # Draw foreground
                        if health_pct > 0:
                            pygame.draw.rect(
                                self.screen,
                                hp_color,
                                (bar_x, bar_y, int(bar_width * health_pct), bar_height),
                            )
                        # Draw border (black)
                        pygame.draw.rect(
                            self.screen,
                            (0, 0, 0),
                            (bar_x, bar_y, bar_width, bar_height),
                            1,
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
            ch = self._get_rendered_surface(arrow, (0, 255, 0))
            cam_x = (tx - self.camera.x) * config.GRID_SIZE * self.camera.zoom
            cam_y = (ty - self.camera.y) * config.GRID_SIZE * self.camera.zoom
            self.screen.blit(ch, (cam_x, cam_y))
            prev_x, prev_y = tx, ty

        tx, ty = tiles[-1]
        final_char = "X"
        ch = self._get_rendered_surface(final_char, (255, 0, 0))
        cam_x = (tx - self.camera.x) * config.GRID_SIZE * self.camera.zoom
        cam_y = (ty - self.camera.y) * config.GRID_SIZE * self.camera.zoom
        self.screen.blit(ch, (cam_x, cam_y))

    @staticmethod
    def _direct_line(start: tuple[int, int], end: tuple[int, int]) -> list[tuple[int, int]]:
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
        # pylint: disable=too-many-return-statements
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
