import pygame
from . import config

class FogOfWar:
    """
    Manages the fog of war overlay for the game map.
    """
    HIDDEN = 0
    EXPLORED = 1
    VISIBLE = 2

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid = [[self.HIDDEN for _ in range(width)] for _ in range(height)]
        self.surface = pygame.Surface(
            (width * config.GRID_SIZE, height * config.GRID_SIZE),
            pygame.SRCALPHA,
        )

    def update(self, units: list) -> None:
        """
        Update the fog of war based on unit positions and vision ranges.
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
            for x in range(max(0, ux - vision_radius), min(self.width, ux + vision_radius + 1)):
                for y in range(max(0, uy - vision_radius), min(self.height, uy + vision_radius + 1)):
                    # Use squared distance to avoid expensive sqrt
                    dist_sq = (x - ux)**2 + (y - uy)**2
                    if dist_sq <= vision_radius**2:
                        self.grid[y][x] = self.VISIBLE

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draw the fog of war onto the screen.
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
