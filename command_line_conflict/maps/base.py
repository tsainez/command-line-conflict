from __future__ import annotations

from heapq import heappop, heappush
from typing import Dict, List, Tuple

import pygame

from .. import config


TERRAIN_NORMAL = 0
TERRAIN_ROUGH = 1
TERRAIN_HIGH_GROUND = 2


class Map:
    """Represents the game map, including walls and pathfinding.

    Attributes:
        width: The width of the map in grid cells.
        height: The height of the map in grid cells.
        walls: A set of (x, y) tuples representing wall locations.
        terrain: A dictionary mapping (x, y) tuples to terrain types.
    """

    def __init__(self, width: int = 40, height: int = 30) -> None:
        """Initializes the map.

        Args:
            width: The width of the map.
            height: The height of the map.
        """
        self.width = width
        self.height = height
        self.walls: set[Tuple[int, int]] = set()
        self.terrain: Dict[Tuple[int, int], int] = {}

    def set_terrain(self, x: int, y: int, terrain_type: int) -> None:
        """Sets the terrain type at the specified coordinates.

        Args:
            x: The x-coordinate.
            y: The y-coordinate.
            terrain_type: The type of terrain (TERRAIN_* constant).
        """
        self.terrain[(x, y)] = terrain_type

    def get_terrain(self, x: int, y: int) -> int:
        """Gets the terrain type at the specified coordinates.

        Args:
            x: The x-coordinate.
            y: The y-coordinate.

        Returns:
            The terrain type, defaulting to TERRAIN_NORMAL.
        """
        return self.terrain.get((x, y), TERRAIN_NORMAL)

    def add_wall(self, x: int, y: int) -> None:
        """Adds a wall at the specified coordinates.

        Args:
            x: The x-coordinate of the wall.
            y: The y-coordinate of the wall.
        """
        self.walls.add((x, y))

    def is_blocked(self, x: int, y: int) -> bool:
        """Checks if a tile is blocked by a wall.

        Args:
            x: The x-coordinate to check.
            y: The y-coordinate to check.

        Returns:
            True if the tile is blocked, False otherwise.
        """
        return (x, y) in self.walls

    def find_path(
        self,
        start: Tuple[int, int],
        goal: Tuple[int, int],
        can_fly: bool = False,
        extra_obstacles: set[Tuple[int, int]] | None = None,
    ) -> List[Tuple[int, int]]:
        """Finds a path between two points using A* algorithm.

        This method can account for flying units and dynamic obstacles.

        Args:
            start: The starting (x, y) coordinates.
            goal: The destination (x, y) coordinates.
            can_fly: If True, the path ignores walls.
            extra_obstacles: A set of additional (x, y) coordinates to treat
                             as obstacles for this pathfinding request.

        Returns:
            A list of (x, y) tuples representing the path from start to goal.
            Returns an empty list if no path is found.
        """
        if not can_fly and self.is_blocked(*goal):
            return []

        open_set: List[Tuple[int, Tuple[int, int]]] = []
        heappush(open_set, (0, start))
        came_from: Dict[Tuple[int, int], Tuple[int, int]] = {}
        g_score = {start: 0}

        while open_set:
            _, current = heappop(open_set)
            if current == goal:
                path = []
                while current != start:
                    path.append(current)
                    current = came_from[current]
                path.reverse()
                return path

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = current[0] + dx, current[1] + dy
                if not (0 <= nx < self.width and 0 <= ny < self.height):
                    continue
                if (
                    not can_fly
                    and self.is_blocked(nx, ny)
                    or (extra_obstacles and (nx, ny) in extra_obstacles)
                ):
                    continue
                movement_cost = 1
                if self.get_terrain(nx, ny) == TERRAIN_ROUGH:
                    movement_cost = 1.33

                tentative_g = g_score[current] + movement_cost
                if (nx, ny) not in g_score or tentative_g < g_score[(nx, ny)]:
                    g_score[(nx, ny)] = tentative_g
                    f = tentative_g + abs(nx - goal[0]) + abs(ny - goal[1])
                    heappush(open_set, (f, (nx, ny)))
                    came_from[(nx, ny)] = current

        return []

    def draw(self, surf, font, camera=None) -> None:
        """Draws the map walls to a surface, using camera if provided.

        Args:
            surf: The pygame surface to draw on.
            font: The pygame font to use for rendering the walls.
            camera: The camera object for view/zoom (optional).
        """
        grid_size = config.GRID_SIZE
        if camera:
            grid_size = int(config.GRID_SIZE * camera.zoom)

        # Draw terrain
        for (x, y), terrain_type in self.terrain.items():
            if terrain_type == TERRAIN_NORMAL:
                continue

            char = ""
            color = (255, 255, 255)
            if terrain_type == TERRAIN_ROUGH:
                char = ","
                color = (150, 100, 50)
            elif terrain_type == TERRAIN_HIGH_GROUND:
                char = "^"
                color = (200, 200, 200)

            if char:
                if camera:
                    draw_x = (x - camera.x) * config.GRID_SIZE * camera.zoom
                    draw_y = (y - camera.y) * config.GRID_SIZE * camera.zoom
                else:
                    draw_x = x * config.GRID_SIZE
                    draw_y = y * config.GRID_SIZE

                ch = font.render(char, True, color)
                ch = pygame.transform.scale(ch, (grid_size, grid_size))
                surf.blit(ch, (draw_x, draw_y))

        for x, y in self.walls:
            if camera:
                draw_x = (x - camera.x) * config.GRID_SIZE * camera.zoom
                draw_y = (y - camera.y) * config.GRID_SIZE * camera.zoom
            else:
                draw_x = x * config.GRID_SIZE
                draw_y = y * config.GRID_SIZE
            ch = font.render("#", True, (100, 100, 100))
            ch = pygame.transform.scale(ch, (grid_size, grid_size))
            surf.blit(ch, (draw_x, draw_y))
