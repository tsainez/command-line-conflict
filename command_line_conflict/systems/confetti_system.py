from ..components.confetti import Confetti
from ..game_state import GameState


class ConfettiSystem:
    """Handles the lifecycle of confetti effects."""

    def update(self, game_state: GameState, dt: float) -> None:
        """Updates the lifetime of all confetti effects.
        Args:
            game_state: The current state of the game.
            dt: The time elapsed since the last frame.
        """
        for entity_id, components in list(game_state.entities.items()):
            confetti = components.get(Confetti)
            if not confetti:
                continue

            confetti.lifetime -= dt
            if confetti.lifetime <= 0:
                del game_state.entities[entity_id]
