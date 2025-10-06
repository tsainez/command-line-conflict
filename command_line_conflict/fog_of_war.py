import pygame

from . import config

# TODO: Integrate logger for debug mode. Currently not used.


class FogOfWar:
    """Manages the fog of war overlay, revealing the map based on unit vision.

    This class maintains a grid representing the visibility state of each map
    tile (hidden, explored, or visible) and provides methods to update and
    draw the fog of war.

    Attributes:
        width (int): The width of the map in grid cells.
        height (int): The height of the map in grid cells.
        grid (list[list[int]]): A 2D list representing the fog of war state for
            each tile.
        surface (pygame.Surface): A surface used for drawing the fog of war overlay.
        HIDDEN (int): A constant representing a hidden tile.
        EXPLORED (int): A constant representing an explored but not visible tile.
        VISIBLE (int): A constant representing a currently visible tile.
    """

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

        This method first downgrades all currently visible tiles to "explored" status.
        Then, it iterates through the provided units, marking the tiles within each
        unit's vision range as "visible".

        Args:
            units: A list of entities that provide vision. Each entity is expected
                   to have Position and Vision components.
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

    def draw(self, screen: pygame.Surface, camera=None) -> None:
        """Draws the fog of war overlay onto the screen, using camera if provided.

        Hidden tiles are drawn as black, and explored tiles are drawn as a
        semi-transparent black. Visible tiles are not drawn, allowing the
        underlying map to be seen.

        Args:
            screen: The pygame screen surface to draw on.
            camera: The camera object for view/zoom (optional).
        """
        self.surface.fill((0, 0, 0, 0))  # Clear the surface with transparency
        grid_size = config.GRID_SIZE
        for y in range(self.height):
            for x in range(self.width):
                draw_x, draw_y = x, y
                size = grid_size
                if camera:
                    draw_x = (x - camera.x) * grid_size * camera.zoom
                    draw_y = (y - camera.y) * grid_size * camera.zoom
                    size = int(grid_size * camera.zoom)
                rect = (
                    draw_x,
                    draw_y,
                    size,
                    size,
                )
                if self.grid[y][x] == self.HIDDEN:
                    pygame.draw.rect(self.surface, (0, 0, 0, 255), rect)
                elif self.grid[y][x] == self.EXPLORED:
                    pygame.draw.rect(self.surface, (0, 0, 0, 180), rect)

        screen.blit(self.surface, (0, 0))
