from .. import config
from .base import AirUnit


class Airplane(AirUnit):
    """Simple flying unit."""

    icon = "A"

    def draw(self, surf, font) -> None:
        color = (0, 255, 255) if self.selected else (200, 200, 200)
        ch = font.render(self.icon, True, color)
        surf.blit(ch, (int(self.x) * config.GRID_SIZE, int(self.y) * config.GRID_SIZE))
