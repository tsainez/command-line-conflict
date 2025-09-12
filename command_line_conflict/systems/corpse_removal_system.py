from ..game_state import GameState
from ..components.dead import Dead


class CorpseRemovalSystem:
    """
    This system is responsible for removing dead units from the game after a
    certain amount of time.
    """

    def __init__(self, corpse_lifetime: float = 5.0):
        self.corpse_lifetime = corpse_lifetime

    def update(self, game_state: GameState, dt: float) -> None:
        for entity_id, components in list(game_state.entities.items()):
            dead = components.get(Dead)
            if dead:
                dead.timer += dt
                if dead.timer >= self.corpse_lifetime:
                    game_state.remove_entity(entity_id)
