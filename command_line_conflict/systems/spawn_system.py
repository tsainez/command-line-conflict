import random

from .. import factories
from ..game_state import GameState


class SpawnSystem:
    """Manages spawning of neutral units."""

    def __init__(self, spawn_interval: float = 10.0):
        """Initializes the SpawnSystem.

        Args:
            spawn_interval: Time in seconds between spawns.
        """
        self.spawn_interval = spawn_interval
        self.time_since_last_spawn = 0.0

    def update(self, game_state: GameState, dt: float) -> None:
        """Processes spawning logic.

        Args:
            game_state: The current state of the game.
            dt: The time elapsed since the last frame.
        """
        self.time_since_last_spawn += dt

        if self.time_since_last_spawn >= self.spawn_interval:
            self.spawn_wildlife(game_state)
            self.time_since_last_spawn = 0.0

    def spawn_wildlife(self, game_state: GameState) -> None:
        """Spawns a wildlife unit at a random valid location."""
        width = game_state.map.width
        height = game_state.map.height

        # Try to find a valid spot
        for _ in range(10):  # 10 attempts
            x = random.randint(0, width - 1)
            y = random.randint(0, height - 1)

            if game_state.map.is_walkable(x, y):
                # Check if occupied by another entity
                if not game_state.get_entities_at_position(x, y):
                    factories.create_wildlife(game_state, float(x), float(y))
                    return
