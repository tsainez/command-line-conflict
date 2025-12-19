import pygame

from . import config
from .logger import log


class FogOfWar:
    """Manages the fog of war overlay, revealing the map based on unit vision."""

    HIDDEN = 0
    EXPLORED = 1
    VISIBLE = 2

    def __init__(self, width: int, height: int):
        """Initializes the FogOfWar system.

        Args:
            width: The width of the map in grid cells.
            height: The height of the map in grid cells.
        """
        self.width = width
        self.height = height
        self.grid = [[self.HIDDEN for _ in range(width)] for _ in range(height)]
        self.surface = None
        self.visible_cells = set()
        self._vision_cache = {}
        log.info(f"Initialized FogOfWar with grid size {width}x{height}")

    def _get_vision_offsets(self, radius: int) -> list[tuple[int, int]]:
        if radius not in self._vision_cache:
            offsets = []
            r2 = radius * radius
            for dy in range(-radius, radius + 1):
                for dx in range(-radius, radius + 1):
                    if dx * dx + dy * dy <= r2:
                        offsets.append((dx, dy))
            self._vision_cache[radius] = offsets
        return self._vision_cache[radius]

    def update(self, units: list) -> None:
        """Updates the fog of war based on unit positions and vision.

        First, it downgrades all currently visible tiles to explored. Then, it
        marks the tiles within each unit's vision range as visible.

        Args:
            units: A list of unit objects that have vision. Each unit must have
                   x, y, and vision_range attributes.
        """
        # Step 1: Downgrade all previously VISIBLE tiles to EXPLORED
        for x, y in self.visible_cells:
            self.grid[y][x] = self.EXPLORED
        self.visible_cells.clear()

        # Step 2: Mark tiles within unit vision as VISIBLE
        for unit in units:
            ux, uy = int(unit.x), int(unit.y)
            vision_range = int(unit.vision_range)

            offsets = self._get_vision_offsets(vision_range)

            for dx, dy in offsets:
                x, y = ux + dx, uy + dy
                if 0 <= x < self.width and 0 <= y < self.height:
                    self.grid[y][x] = self.VISIBLE
                    self.visible_cells.add((x, y))

    def draw(self, screen: pygame.Surface, camera=None) -> None:
        """Draws the fog of war overlay onto the screen, using camera if provided.

        Hidden tiles are drawn as black, and explored tiles are drawn as a
        semi-transparent black. Visible tiles are not drawn, allowing the
        underlying map to be seen.

        Args:
            screen: The pygame screen surface to draw on.
            camera: The camera object for view/zoom (optional).
        """
        if self.surface is None or self.surface.get_size() != screen.get_size():
            log.debug(f"Creating FogOfWar surface with size {screen.get_size()}")
            self.surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)

        # Fill with opaque black (HIDDEN)
        self.surface.fill((0, 0, 0, 255))

        grid_size = config.GRID_SIZE
        screen_w, screen_h = screen.get_size()

        # Calculate visible grid bounds to avoid iterating over the entire map
        start_x, start_y = 0, 0
        end_x, end_y = self.width, self.height

        if camera:
            scaled_grid_size = int(grid_size * camera.zoom)
            if scaled_grid_size > 0:
                start_x = int(camera.x)
                end_x = int(camera.x + screen_w / scaled_grid_size) + 2
                start_y = int(camera.y)
                end_y = int(camera.y + screen_h / scaled_grid_size) + 2
        else:
            if grid_size > 0:
                end_x = int(screen_w / grid_size) + 2
                end_y = int(screen_h / grid_size) + 2

        # Clamp to map bounds
        start_x = max(0, start_x)
        end_x = min(self.width, end_x)
        start_y = max(0, start_y)
        end_y = min(self.height, end_y)

        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                state = self.grid[y][x]
                if state == self.HIDDEN:
                    continue

                draw_x, draw_y = x, y
                size = grid_size
                if camera:
                    draw_x = (x - camera.x) * grid_size * camera.zoom
                    draw_y = (y - camera.y) * grid_size * camera.zoom
                    size = int(grid_size * camera.zoom)
                else:
                    draw_x *= grid_size
                    draw_y *= grid_size

                # Ensure we draw integers for rect
                rect = (int(draw_x), int(draw_y), size + 1, size + 1)

                if state == self.VISIBLE:
                    self.surface.fill((0, 0, 0, 0), rect)
                elif state == self.EXPLORED:
                    self.surface.fill((0, 0, 0, 180), rect)

        screen.blit(self.surface, (0, 0))
