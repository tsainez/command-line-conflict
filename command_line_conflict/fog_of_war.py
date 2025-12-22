import pygame

from . import config
from .logger import log


class FogOfWar:
    """Manages the fog of war overlay, revealing the map based on unit vision.

    Optimized to use a persistent texture and differential updates.
    """

    HIDDEN = 0
    EXPLORED = 1
    VISIBLE = 2

    # Colors for the fog texture
    COLOR_HIDDEN = (0, 0, 0, 255)
    COLOR_EXPLORED = (0, 0, 0, 180)
    COLOR_VISIBLE = (0, 0, 0, 0)

    def __init__(self, width: int, height: int):
        """Initializes the FogOfWar system.

        Args:
            width: The width of the map in grid cells.
            height: The height of the map in grid cells.
        """
        self.width = width
        self.height = height
        # Logic grid
        self.grid = [[self.HIDDEN for _ in range(width)] for _ in range(height)]

        # Visual texture (1 pixel per tile)
        self.fog_texture = pygame.Surface((width, height), pygame.SRCALPHA)
        self.fog_texture.fill(self.COLOR_HIDDEN)

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

        Args:
            units: A list of unit objects that have vision. Each unit must have
                   x, y, and vision_range attributes.
        """
        # Calculate currently visible cells
        current_visible = set()

        for unit in units:
            ux, uy = int(unit.x), int(unit.y)
            vision_range = int(unit.vision_range)

            offsets = self._get_vision_offsets(vision_range)

            for dx, dy in offsets:
                x, y = ux + dx, uy + dy
                if 0 <= x < self.width and 0 <= y < self.height:
                    current_visible.add((x, y))

        # Determine what changed
        to_explore = self.visible_cells - current_visible
        to_reveal = current_visible - self.visible_cells

        # If nothing changed, we are done
        if not to_explore and not to_reveal:
            return

        # Update grid and texture
        # Using PixelArray for faster pixel access
        try:
            px = pygame.PixelArray(self.fog_texture)

            for x, y in to_explore:
                self.grid[y][x] = self.EXPLORED
                px[x, y] = self.COLOR_EXPLORED

            for x, y in to_reveal:
                self.grid[y][x] = self.VISIBLE
                px[x, y] = self.COLOR_VISIBLE

            # No need to explicitly delete px, context manager or del works
            del px
        except Exception as e:  # pylint: disable=broad-except
            log.error(f"Error updating fog texture: {e}")

        # Update state
        self.visible_cells = current_visible

    def draw(self, screen: pygame.Surface, camera=None) -> None:
        """Draws the fog of war overlay onto the screen.

        Scales the fog texture to match the screen view.

        Args:
            screen: The pygame screen surface to draw on.
            camera: The camera object for view/zoom (optional).
        """
        grid_size = config.GRID_SIZE
        screen_w, screen_h = screen.get_size()

        if camera:
            # Determine visible portion of the map in grid coordinates
            # Camera view in pixels:
            # The map is drawn at: (x - cam.x) * tile_size * zoom
            # We want to find the source rect in the texture corresponding to the screen.

            zoom = camera.zoom
            scaled_tile_size = grid_size * zoom

            # Map top-left on screen
            # map_screen_x = -camera.x * scaled_tile_size
            # map_screen_y = -camera.y * scaled_tile_size

            # Better: Subsurface the visible part of the texture, then scale it.

            start_x = int(camera.x)
            start_y = int(camera.y)
            # Add buffer
            width_tiles = int(screen_w / scaled_tile_size) + 2
            height_tiles = int(screen_h / scaled_tile_size) + 2

            # Clamp
            start_x = max(0, min(start_x, self.width))
            start_y = max(0, min(start_y, self.height))

            end_x = min(self.width, start_x + width_tiles)
            end_y = min(self.height, start_y + height_tiles)

            w = end_x - start_x
            h = end_y - start_y

            if w <= 0 or h <= 0:
                return

            # Extract source patch
            sub = self.fog_texture.subsurface((start_x, start_y, w, h))

            # Target size
            target_w = int(w * scaled_tile_size)
            target_h = int(h * scaled_tile_size)

            # Scale
            scaled = pygame.transform.scale(sub, (target_w, target_h))

            # Blit position
            # (start_x - camera.x) * scaled_tile_size
            pos_x = (start_x - camera.x) * scaled_tile_size
            pos_y = (start_y - camera.y) * scaled_tile_size

            screen.blit(scaled, (pos_x, pos_y))

        else:
            # Full map fit to screen? Or just scale by grid size?
            # Original code: if no camera, just scale by grid_size starting at 0,0
            target_w = self.width * grid_size
            target_h = self.height * grid_size

            scaled = pygame.transform.scale(self.fog_texture, (target_w, target_h))
            screen.blit(scaled, (0, 0))
