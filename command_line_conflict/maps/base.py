from heapq import heappop, heappush
from typing import Dict, List, Tuple

from .. import config
from ..units import Unit


class Map:
    """Container for units present in a level."""

    def __init__(self, width: int = 40, height: int = 30) -> None:
        self.width = width
        self.height = height
        self.units: List[Unit] = []
        self.walls: set[Tuple[int, int]] = set()

    def spawn_unit(self, unit: Unit) -> None:
        self.units.append(unit)

    def add_wall(self, x: int, y: int) -> None:
        self.walls.add((x, y))

    def is_blocked(self, x: int, y: int) -> bool:
        return (x, y) in self.walls

    def find_path(
        self, start: Tuple[int, int], goal: Tuple[int, int]
    ) -> List[Tuple[int, int]]:
        """A* pathfinding ignoring dynamic obstacles."""
        if self.is_blocked(*goal):
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
                if self.is_blocked(nx, ny):
                    continue
                tentative_g = g_score[current] + 1
                if (nx, ny) not in g_score or tentative_g < g_score[(nx, ny)]:
                    g_score[(nx, ny)] = tentative_g
                    f = tentative_g + abs(nx - goal[0]) + abs(ny - goal[1])
                    heappush(open_set, (f, (nx, ny)))
                    came_from[(nx, ny)] = current

        return []

    def update(self, dt: float) -> None:
        for u in list(self.units):
            u.update(dt, self)

    def draw(self, surf, font) -> None:
        for x, y in self.walls:
            ch = font.render("#", True, (100, 100, 100))
            surf.blit(ch, (x * config.GRID_SIZE, y * config.GRID_SIZE))
