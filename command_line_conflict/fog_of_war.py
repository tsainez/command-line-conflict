import pygame
from . import config


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
        self.surface = pygame.Surface(
            (width * config.GRID_SIZE, height * config.GRID_SIZE),
            pygame.SRCALPHA,
        )

    def update(self, units: list) -> None:
        """Updates the fog of war based on unit positions and vision.

        First, it downgrades all currently visible tiles to explored. Then, it
        marks the tiles within each unit's vision range as visible.

        Args:
            units: A list of unit objects that have vision. Each unit must have
                   x, y, and vision_range attributes.
        """
        # Step 1: Downgrade all VISIBLE tiles to EXPLORED
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] == self.VISIBLE:
                    self.grid[y][x] = self.EXPLORED

        # Step 2: Mark tiles within unit vision as VISIBLE
        for unit in units:
            ux, uy = int(unit.x), int(unit.y)
            vision_radius = unit.vision_range
            # Iterate over a square bounding box around the unit's vision circle
            for x in range(
                max(0, ux - vision_radius), min(self.width, ux + vision_radius + 1)
            ):
                for y in range(
                    max(0, uy - vision_radius), min(self.height, uy + vision_radius + 1)
                ):
                    # Use squared distance to avoid expensive sqrt
                    dist_sq = (x - ux) ** 2 + (y - uy) ** 2
                    if dist_sq <= vision_radius**2:
                        self.grid[y][x] = self.VISIBLE

    def draw(self, screen: pygame.Surface) -> None:
        """Draws the fog of war overlay onto the screen.

        Hidden tiles are drawn as black, and explored tiles are drawn as a
        semi-transparent black. Visible tiles are not drawn, allowing the
        underlying map to be seen.

        Args:
            screen: The pygame screen surface to draw on.
        """
        self.surface.fill((0, 0, 0, 0))  # Clear the surface with transparency
        for y in range(self.height):
            for x in range(self.width):
                rect = (
                    x * config.GRID_SIZE,
                    y * config.GRID_SIZE,
                    config.GRID_SIZE,
                    config.GRID_SIZE,
                )
                if self.grid[y][x] == self.HIDDEN:
                    pygame.draw.rect(self.surface, (0, 0, 0, 255), rect)
                elif self.grid[y][x] == self.EXPLORED:
                    pygame.draw.rect(self.surface, (0, 0, 0, 180), rect)

        screen.blit(self.surface, (0, 0))
