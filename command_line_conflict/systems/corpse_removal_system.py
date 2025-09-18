from ..components.dead import Dead
from ..game_state import GameState

# TODO: Integrate logger for debug mode. Currently not used.
#       Consider logging when corpses are removed for debugging purposes.


class CorpseRemovalSystem:
    """Removes dead entities from the game after a specified time."""

    def __init__(self, corpse_lifetime: float = 5.0):
        """Initializes the CorpseRemovalSystem.

        Args:
            corpse_lifetime: The time in seconds before a corpse is removed.
        """
        self.corpse_lifetime = corpse_lifetime

    def update(self, game_state: GameState, dt: float) -> None:
        """Updates the timer on dead entities and removes them if expired.

        Args:
            game_state: The current state of the game.
            dt: The time elapsed since the last frame.
        """
        for entity_id, components in list(game_state.entities.items()):
            dead = components.get(Dead)
            if dead:
                dead.timer += dt
                if dead.timer >= self.corpse_lifetime:
                    game_state.remove_entity(entity_id)
