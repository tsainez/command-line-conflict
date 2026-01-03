from __future__ import annotations

import os
from heapq import heappop, heappush
from typing import Dict, List, Tuple

import pygame

from .. import config
from ..logger import log


class Map:
    """Represents the game map, including walls and pathfinding.

    Attributes:
        width: The width of the map in grid cells.
        height: The height of the map in grid cells.
        walls: A set of (x, y) tuples representing wall locations.
    """

    MAX_MAP_DIMENSION = 256  # Security limit to prevent DoS via memory exhaustion
    MAX_FILE_SIZE = 2 * 1024 * 1024  # Security limit: 2MB max file size
    MAX_PATHFINDING_ITERATIONS = 50000  # Security limit to prevent pathfinding freeze

    def __init__(self, width: int = 40, height: int = 30) -> None:
        """Initializes the map.

        Args:
            width: The width of the map.
            height: The height of the map.

        Raises:
            ValueError: If dimensions exceed MAX_MAP_DIMENSION.
        """
        if width > self.MAX_MAP_DIMENSION or height > self.MAX_MAP_DIMENSION:
            raise ValueError(f"Map dimensions exceed maximum allowed size ({self.MAX_MAP_DIMENSION})")

        self.width = width
        self.height = height
        self.walls: set[Tuple[int, int]] = set()

    def add_wall(self, x: int, y: int) -> None:
        """Adds a wall at the specified coordinates.

        Args:
            x: The x-coordinate of the wall.
            y: The y-coordinate of the wall.
        """
        if 0 <= x < self.width and 0 <= y < self.height:
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

    def find_path(  # pylint: disable=too-many-positional-arguments
        self,
        start: Tuple[int, int],
        goal: Tuple[int, int],
        can_fly: bool = False,
        extra_obstacles: set[Tuple[int, int]] | dict | None = None,
        exclude_obstacles: set[Tuple[int, int]] | None = None,
    ) -> List[Tuple[int, int]]:
        """Finds a path between two points using A* algorithm.

        This method can account for flying units and dynamic obstacles.

        Args:
            start: The starting (x, y) coordinates.
            goal: The destination (x, y) coordinates.
            can_fly: If True, the path ignores walls.
            extra_obstacles: A set or dict of additional (x, y) coordinates to treat
                             as obstacles.
            exclude_obstacles: A set of coordinates to ignore if they appear in extra_obstacles.

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

        iterations = 0

        while open_set:
            # Security: Prevent infinite loops or excessive CPU usage
            iterations += 1
            if iterations > self.MAX_PATHFINDING_ITERATIONS:
                log.warning(f"Pathfinding iteration limit reached ({self.MAX_PATHFINDING_ITERATIONS}). Aborting.")
                return []

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

                if not can_fly and self.is_blocked(nx, ny):
                    continue

                if extra_obstacles and (nx, ny) in extra_obstacles:
                    if not (exclude_obstacles and (nx, ny) in exclude_obstacles):
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

    def to_dict(self) -> dict:
        """Converts the map data to a dictionary for serialization.

        Returns:
            A dictionary representation of the map.
        """
        return {
            "width": self.width,
            "height": self.height,
            "walls": list(self.walls),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Map":
        """Creates a Map instance from a dictionary.

        Args:
            data: The dictionary containing map data.

        Returns:
            A new Map instance.
        """
        m = cls(width=data["width"], height=data["height"])

        # Security: Validate walls are within bounds and well-formed
        walls = set()
        raw_walls = data.get("walls", [])
        if not isinstance(raw_walls, list):
            raw_walls = []

        # Security: Prevent CPU exhaustion from excessive wall definitions
        max_walls = m.width * m.height
        if len(raw_walls) > max_walls:
            log.warning(f"Too many walls defined ({len(raw_walls)}). Truncating to {max_walls}.")
            raw_walls = raw_walls[:max_walls]

        for w in raw_walls:
            if isinstance(w, (list, tuple)) and len(w) >= 2:
                # Ensure coordinates are integers
                try:
                    x = int(w[0])
                    y = int(w[1])
                    if 0 <= x < m.width and 0 <= y < m.height:
                        walls.add((x, y))
                except (ValueError, TypeError):
                    continue

        m.walls = walls
        return m

    def save_to_file(self, filename: str) -> None:
        """Saves the map to a JSON file.

        Args:
            filename: The path to the file to save to.

        Raises:
            ValueError: If the filename is outside authorized directories.
        """
        import json

        from ..utils.paths import get_user_data_dir

        # Security fix: Path traversal prevention
        # Resolve symlinks to ensure we check the actual destination
        abs_path = os.path.realpath(filename)

        # Define allowed directories
        # 1. The maps directory (where this file resides)
        maps_dir = os.path.realpath(os.path.dirname(os.path.abspath(__file__)))

        # 2. The user data directory
        user_data_dir = str(get_user_data_dir())
        # Ensure user_data_dir is also resolved if it's a symlink
        user_data_dir = os.path.realpath(user_data_dir)

        allowed_dirs = [maps_dir, user_data_dir]

        is_allowed = False
        for allowed_dir in allowed_dirs:
            try:
                # os.path.commonpath returns the longest common sub-path
                if os.path.commonpath([allowed_dir, abs_path]) == allowed_dir:
                    is_allowed = True
                    break
            except ValueError:
                continue

        if not is_allowed:
            log.error(f"Security violation: Attempted to save map to unauthorized location: {abs_path}")
            raise ValueError(f"Cannot save to unauthorized location: {filename}")

        # Ensure directory exists
        os.makedirs(os.path.dirname(abs_path), exist_ok=True)

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=4)

    @classmethod
    def load_from_file(cls, filename: str) -> "Map":
        """Loads a map from a JSON file.

        Args:
            filename: The path to the file to load from.

        Returns:
            The loaded Map instance.

        Raises:
            ValueError: If the file size exceeds MAX_FILE_SIZE or is a special file.
        """
        import json
        import stat

        try:
            st = os.stat(filename)
        except OSError as e:
            raise ValueError(f"Could not stat file: {e}") from e

        # Security: Check file type to prevent reading from special files (e.g., /dev/zero)
        # which can cause DoS.
        if not stat.S_ISREG(st.st_mode):
            raise ValueError("Map file must be a regular file.")

        # Security: Check file size to prevent DoS via memory exhaustion
        if st.st_size > cls.MAX_FILE_SIZE:
            raise ValueError(f"Map file exceeds maximum allowed size ({cls.MAX_FILE_SIZE} bytes)")

        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        return cls.from_dict(data)
