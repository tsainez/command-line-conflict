from .. import config
from .base import Unit


class Airplane(Unit):
    """Example of a different type of Unit."""

    def draw(self, surf, font) -> None:
        color = (0, 255, 255) if self.selected else (200, 200, 200)
        ch = font.render("A", True, color)
        surf.blit(ch, (int(self.x) * config.GRID_SIZE, int(self.y) * config.GRID_SIZE))
