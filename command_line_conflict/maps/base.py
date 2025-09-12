from __future__ import annotations

from heapq import heappop, heappush
from typing import Dict, List, Tuple

from .. import config


class Map:
    """Container for units present in a level."""

    def __init__(self, width: int = 40, height: int = 30) -> None:
        self.width = width
        self.height = height
        self.walls: set[Tuple[int, int]] = set()

    def add_wall(self, x: int, y: int) -> None:
        self.walls.add((x, y))

    def is_blocked(self, x: int, y: int) -> bool:
        return (x, y) in self.walls

    def find_path(
        self,
        start: Tuple[int, int],
        goal: Tuple[int, int],
        can_fly: bool = False,
        extra_obstacles: set[Tuple[int, int]] | None = None,
    ) -> List[Tuple[int, int]]:
        """A* pathfinding that can account for dynamic obstacles."""
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

    def draw(self, surf, font, camera) -> None:
        zoomed_grid_size = int(config.GRID_SIZE * camera.zoom)
        if zoomed_grid_size <= 0:
            return

        zoomed_font = pygame.font.Font(font.get_path(), zoomed_grid_size)

        for x, y in self.walls:
            ch = zoomed_font.render("#", True, (100, 100, 100))
            screen_pos = camera.world_to_screen(
                x * config.GRID_SIZE, y * config.GRID_SIZE
            )
            surf.blit(ch, screen_pos)
