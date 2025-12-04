from __future__ import annotations

from heapq import heappop, heappush
from typing import Dict, List, Tuple

import pygame

from .. import config


class Map:
    """Represents the game map, including walls and pathfinding.

    Attributes:
        width: The width of the map in grid cells.
        height: The height of the map in grid cells.
        walls: A set of (x, y) tuples representing wall locations.
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

    def is_walkable(self, x: int, y: int) -> bool:
        """Checks if a tile is valid and not blocked.

        Args:
            x: The x-coordinate to check.
            y: The y-coordinate to check.

        Returns:
            True if the tile is walkable, False otherwise.
        """
        if not (0 <= x < self.width and 0 <= y < self.height):
            return False
        return not self.is_blocked(x, y)

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
                tentative_g = g_score[current] + 1
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
        for x, y in self.walls:
            grid_size = config.GRID_SIZE
            if camera:
                draw_x = (x - camera.x) * config.GRID_SIZE * camera.zoom
                draw_y = (y - camera.y) * config.GRID_SIZE * camera.zoom
                grid_size = int(config.GRID_SIZE * camera.zoom)
            else:
                draw_x = x * grid_size
                draw_y = y * grid_size
            ch = font.render("#", True, (100, 100, 100))
            ch = pygame.transform.scale(ch, (grid_size, grid_size))
            surf.blit(ch, (draw_x, draw_y))
