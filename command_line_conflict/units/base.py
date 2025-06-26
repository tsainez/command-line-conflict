from .. import config


class Unit:
    """A basic unit that can move around the grid."""

    def __init__(self, x: float, y: float) -> None:
        self.x = float(x)
        self.y = float(y)
        self.target_x = self.x
        self.target_y = self.y
        self.selected = False

    def update(self, dt: float) -> None:
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
        ch = font.render("U", True, color)
        surf.blit(ch, (int(self.x) * config.GRID_SIZE, int(self.y) * config.GRID_SIZE))
