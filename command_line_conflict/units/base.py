from .. import config

# Flag toggled by the engine to decide whether ASCII graphics should be used
USE_ASCII = False


class Unit:
    """Base unit class."""

    icon = "U"
    max_hp = 100
    attack_range = 5
    speed = 2

    def __init__(self, x: float, y: float) -> None:
        self.x = float(x)
        self.y = float(y)
        self.hp = self.max_hp
        self.target_x = self.x
        self.target_y = self.y
        self.selected = False
        self.path: list[tuple[int, int]] = []
        # Remember the last commanded destination so it persists even if
        # the intermediate path is consumed while moving.
        self.order_target: tuple[int, int] | None = None

    def is_air(self) -> bool:  # pragma: no cover - tiny helper
        return False

    def set_target(self, x: int, y: int, game_map=None) -> None:
        self.target_x = x
        self.target_y = y
        self.path = []
        self.order_target = (x, y)

    def update(self, dt: float, game_map=None) -> None:
        """Move the unit toward its target."""
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        dist = (dx * dx + dy * dy) ** 0.5
        if dist < 0.01:
            return
        step = self.speed * dt
        if step > dist:
            step = dist
        self.x += step * dx / dist
        self.y += step * dy / dist

    def draw(self, surf, font) -> None:
        color = (0, 255, 0) if self.selected else (255, 255, 255)
        ch = font.render(self.icon, True, color)
        surf.blit(
            ch,
            (
                int(self.x) * config.GRID_SIZE,
                int(self.y) * config.GRID_SIZE,
            ),
        )

        self.draw_orders(surf, font)

    def draw_orders(self, surf, font) -> None:
        """Render target point and remaining path when selected."""
        if not self.selected:
            return

        # Determine the true final destination for rendering. Ground units
        # overwrite ``target_x``/``target_y`` with intermediate waypoints
        # while moving, so rely on the remembered order target when present.
        if self.path:
            final = self.path[-1]
        elif self.order_target is not None:
            final = (int(self.order_target[0]), int(self.order_target[1]))
        else:
            final = (int(self.target_x), int(self.target_y))

        # If the unit has arrived and has no path, nothing to draw
        if not self.path and final == (int(self.x), int(self.y)):
            return

        # Combine remaining path with final destination. Air units do not have a
        # path list, so approximate a straight line for visualization when
        # ``self.path`` is empty.
        tiles = list(self.path)
        if not tiles:
            tiles = self._direct_line((int(self.x), int(self.y)), final)
        if not tiles or tiles[-1] != final:
            tiles.append(final)

        # draw arrows along remaining path
        prev_x, prev_y = int(self.x), int(self.y)
        for tx, ty in tiles[:-1]:
            arrow = self._arrow_char(tx - prev_x, ty - prev_y)
            ch = font.render(arrow, True, (0, 255, 0))
            surf.blit(ch, (tx * config.GRID_SIZE, ty * config.GRID_SIZE))
            prev_x, prev_y = tx, ty

        # draw final destination
        tx, ty = tiles[-1]
        final_char = "X" if USE_ASCII else "\u2588"
        ch = font.render(final_char, True, (255, 0, 0))
        surf.blit(ch, (tx * config.GRID_SIZE, ty * config.GRID_SIZE))

    @staticmethod
    def _direct_line(start: tuple[int, int], end: tuple[int, int]) -> list[tuple[int, int]]:
        """Return a simple diagonal path from ``start`` to ``end``."""
        x, y = start
        path: list[tuple[int, int]] = []
        while (x, y) != end:
            if x < end[0]:
                x += 1
            elif x > end[0]:
                x -= 1
            if y < end[1]:
                y += 1
            elif y > end[1]:
                y -= 1
            path.append((x, y))
        return path

    @staticmethod
    def _arrow_char(dx: int, dy: int) -> str:
        """Return a character representing movement direction."""
        dx = (dx > 0) - (dx < 0)
        dy = (dy > 0) - (dy < 0)
        if USE_ASCII:
            if dx == 1 and dy == 0:
                return ">"
            if dx == -1 and dy == 0:
                return "<"
            if dx == 0 and dy == 1:
                return "v"
            if dx == 0 and dy == -1:
                return "^"
            if dx == 1 and dy == 1:
                return "\\"
            if dx == -1 and dy == -1:
                return "\\"
            if dx == 1 and dy == -1:
                return "/"
            if dx == -1 and dy == 1:
                return "/"
            if dx != 0:
                return "-"
            if dy != 0:
                return "|"
            return "+"
        else:
            if dx == 1 and dy == 0:
                return "\u2192"  # right arrow
            if dx == -1 and dy == 0:
                return "\u2190"  # left arrow
            if dx == 0 and dy == 1:
                return "\u2193"  # down arrow
            if dx == 0 and dy == -1:
                return "\u2191"  # up arrow
            if dx == 1 and dy == 1:
                return "\u2198"  # down-right
            if dx == -1 and dy == 1:
                return "\u2199"  # down-left
            if dx == 1 and dy == -1:
                return "\u2197"  # up-right
            if dx == -1 and dy == -1:
                return "\u2196"  # up-left
            return "+"


class GroundUnit(Unit):
    """Unit that uses pathfinding and cannot cross walls."""

    icon = "G"

    def set_target(self, x: int, y: int, game_map=None) -> None:
        super().set_target(x, y, game_map)
        if game_map:
            sx, sy = int(self.x), int(self.y)
            self.path = game_map.find_path((sx, sy), (x, y))

    def update(self, dt: float, game_map=None) -> None:
        if self.path:
            next_x, next_y = self.path[0]
            self.target_x, self.target_y = next_x, next_y
            dx = self.target_x - self.x
            dy = self.target_y - self.y
            dist = (dx * dx + dy * dy) ** 0.5
            if dist < 0.01:
                self.x = self.target_x
                self.y = self.target_y
                self.path.pop(0)
            else:
                step = self.speed * dt
                if step > dist:
                    step = dist
                self.x += step * dx / dist
                self.y += step * dy / dist
        else:
            super().update(dt, game_map)


class AirUnit(Unit):
    """Unit that can fly over walls."""

    icon = "A"

    def is_air(self) -> bool:  # pragma: no cover - simple helper
        return True
