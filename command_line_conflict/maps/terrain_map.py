import random
from .base import Map, TERRAIN_HIGH_GROUND, TERRAIN_ROUGH

class TerrainMap(Map):
    """A map with randomly generated terrain."""

    def __init__(self, width: int = 40, height: int = 30) -> None:
        """Initializes the TerrainMap with random terrain."""
        super().__init__(width, height)

        # Seed for reproducibility if needed, but for now purely random is fine
        # random.seed(42)

        # Generate some Rough Terrain patches
        for _ in range(10):
            cx, cy = random.randint(0, width - 1), random.randint(0, height - 1)
            for dx in range(-2, 3):
                for dy in range(-2, 3):
                    nx, ny = cx + dx, cy + dy
                    if 0 <= nx < width and 0 <= ny < height:
                        if random.random() < 0.7:
                             self.set_terrain(nx, ny, TERRAIN_ROUGH)

        # Generate some High Ground patches
        for _ in range(5):
            cx, cy = random.randint(0, width - 1), random.randint(0, height - 1)
            for dx in range(-2, 3):
                for dy in range(-2, 3):
                    nx, ny = cx + dx, cy + dy
                    if 0 <= nx < width and 0 <= ny < height:
                        if random.random() < 0.7:
                             self.set_terrain(nx, ny, TERRAIN_HIGH_GROUND)

        # Add some walls (standard obstacles)
        for _ in range(20):
             wx, wy = random.randint(0, width - 1), random.randint(0, height - 1)
             self.add_wall(wx, wy)
