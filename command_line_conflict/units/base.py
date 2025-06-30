from .. import config


class Unit:
    """Base unit class."""

    icon = "U"

    def __init__(self, x: float, y: float) -> None:
        self.x = float(x)
        self.y = float(y)
        self.target_x = self.x
        self.target_y = self.y
        self.selected = False
        self.path: list[tuple[int, int]] = []

    def is_air(self) -> bool:  # pragma: no cover - tiny helper
        return False

    def set_target(self, x: int, y: int, game_map=None) -> None:
        self.target_x = x
        self.target_y = y
        self.path = []

    def update(self, dt: float, game_map=None) -> None:
        """Move the unit toward its target."""
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        dist = (dx * dx + dy * dy) ** 0.5
        if dist < 0.01:
            return
        step = config.UNIT_SPEED * dt
        if step > dist:
            step = dist
        self.x += step * dx / dist
        self.y += step * dy / dist

    def draw(self, surf, font) -> None:
        color = (0, 255, 0) if self.selected else (255, 255, 255)
        ch = font.render(self.icon, True, color)
        surf.blit(ch, (int(self.x) * config.GRID_SIZE, int(self.y) * config.GRID_SIZE))


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
                step = config.UNIT_SPEED * dt
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
