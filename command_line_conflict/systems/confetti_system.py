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
        # Optimized to iterate only over entities with Confetti component
        # We must iterate over a copy because we might remove entities.
        for entity_id in list(game_state.get_entities_with_component(Confetti)):
            confetti = game_state.get_component(entity_id, Confetti)
            if not confetti:
                continue

            confetti.lifetime -= dt
            if confetti.lifetime <= 0:
                game_state.remove_entity(entity_id)
